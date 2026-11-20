#!/usr/bin/env python3
"""Render a "most used languages" card from the account's own public repositories.

Bytes of code per language (GitHub Linguist, as shown on each repository) are summed across every
public repository the user owns. Forks and archived repositories are excluded so the card reflects
the user's own work. Standard library only; runs in GitHub Actions with the workflow token.

    GITHUB_TOKEN=... python languages.py <user> <out_dir>
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

API = "https://api.github.com/graphql"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
# Notebook outputs are data, not code; they would otherwise dominate the byte count.
EXCLUDE = {s.strip() for s in os.environ.get("LANG_EXCLUDE", "Jupyter Notebook").split(",") if s.strip()}
TOP = 10

THEMES = {
    "dark": dict(panel="#11161f", border="#30363d", text="#e6edf3", muted="#9da7b3", track="#21262d", accent="#58a6ff"),
    "light": dict(panel="#ffffff", border="#d0d7de", text="#1f2328", muted="#57606a", track="#eaeef2", accent="#0969da"),
}

QUERY = """query($login:String!,$after:String){user(login:$login){repositories(first:100,after:$after,
ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false){pageInfo{hasNextPage endCursor}
nodes{name isArchived languages(first:30,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}"""


def gql(query: str, **variables) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]


def fetch(login: str) -> dict:
    totals: dict[str, int] = {}
    colors: dict[str, str] = {}
    repos, after = 0, None
    while True:
        page = gql(QUERY, login=login, after=after)["user"]["repositories"]
        for repo in page["nodes"]:
            if repo["isArchived"]:
                continue
            repos += 1
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                if name in EXCLUDE:
                    continue
                totals[name] = totals.get(name, 0) + edge["size"]
                colors[name] = edge["node"]["color"] or "#8b949e"
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return {"totals": totals, "colors": colors, "repos": repos, "today": dt.date.today().isoformat()}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(data: dict, theme: str) -> str:
    t = THEMES[theme]
    total = sum(data["totals"].values()) or 1
    ranked = sorted(data["totals"].items(), key=lambda kv: -kv[1])
    top = ranked[:TOP]
    other = sum(v for _, v in ranked[TOP:])
    items = [(n, v, data["colors"].get(n, "#8b949e")) for n, v in top]
    if other:
        items.append((f"Other ({len(ranked) - TOP})", other, "#8b949e"))

    width, pad = 840, 24
    bar_y = 72
    out = []
    # stacked overview bar
    x, inner = pad, width - 2 * pad
    out.append(f'<clipPath id="stack"><rect x="{pad}" y="{bar_y}" width="{inner}" height="12" rx="6"/></clipPath>')
    out.append(f'<g clip-path="url(#stack)"><rect x="{pad}" y="{bar_y}" width="{inner}" height="12" fill="{t["track"]}"/>')
    for i, (name, v, c) in enumerate(items):
        w = inner * v / total
        out.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w + 0.5:.1f}" height="12" fill="{c}" class="seg" '
                   f'style="animation-delay:{i * 0.06:.2f}s"><title>{esc(name)} {v / total:.1%}</title></rect>')
        x += w
    out.append("</g>")
    # two columns of rows
    col_w = (width - 2 * pad - 40) / 2
    rows = -(-len(items) // 2)
    top_y = bar_y + 38
    row_h = 36
    for i, (name, v, c) in enumerate(items):
        col, row = divmod(i, rows)
        cx = pad + col * (col_w + 40)
        cy = top_y + row * row_h
        p = v / total
        track_w = col_w - 70
        out.append(f'<circle cx="{cx + 5}" cy="{cy + 5}" r="5" fill="{c}"/>'
                   f'<text x="{cx + 16}" y="{cy + 9.5}" class="n">{esc(name)}</text>'
                   f'<text x="{cx + col_w}" y="{cy + 9.5}" class="p">{p * 100:.2f}%</text>'
                   f'<rect x="{cx}" y="{cy + 17}" width="{track_w + 70}" height="6" rx="3" fill="{t["track"]}"/>'
                   f'<rect x="{cx}" y="{cy + 17}" width="{max(3, (track_w + 70) * p):.1f}" height="6" '
                   f'rx="3" fill="{c}" class="bar" style="animation-delay:{0.3 + i * 0.07:.2f}s"/>')
    height = top_y + rows * row_h + 26
    note = (f"Bytes of code across {data['repos']} public repositories (forks and archived excluded"
            f"{', ' + ', '.join(sorted(EXCLUDE)) + ' not counted' if EXCLUDE else ''}) · updated {data['today']}")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Most used languages: {esc(', '.join(f'{n} {v / total:.1%}' for n, v, _ in items))}">
<title>Most used languages</title>
<style>
.tt{{font:700 18px {FONT};fill:{t['text']}}} .st{{font:400 12px {FONT};fill:{t['muted']}}}
.n{{font:600 13px {FONT};fill:{t['text']}}} .p{{font:500 12.5px {FONT};fill:{t['muted']};text-anchor:end}}
.bar,.seg{{transform-box:fill-box;transform-origin:left;animation:grow 1s cubic-bezier(.2,.7,.2,1) both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion:reduce){{.bar,.seg{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="{pad}" y="38" class="tt">Most used languages</text>
<text x="{pad}" y="58" class="st">{esc(note)}</text>
{''.join(out)}
</svg>
"""


def main() -> None:
    login, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(Path(os.environ["LANG_FIXTURE"]).read_text()) if os.environ.get("LANG_FIXTURE") else fetch(login)
    for theme in THEMES:
        (out / f"languages-{theme}.svg").write_text(render(data, theme))
    total = sum(data["totals"].values()) or 1
    print(", ".join(f"{n} {v / total:.1%}" for n, v in sorted(data["totals"].items(), key=lambda kv: -kv[1])[:TOP]))


if __name__ == "__main__":
    main()
