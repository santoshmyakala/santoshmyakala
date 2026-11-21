#!/usr/bin/env python3
"""Render an all-time GitHub contribution history (every year since the account was created).

Runs in GitHub Actions with the workflow token; writes activity-dark.svg and activity-light.svg.
Standard library only.

    GITHUB_TOKEN=... python activity_history.py <user> <out_dir>
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com/graphql"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
THEMES = {  # GitLab-style indigo activity scale; the snake is GitLab orange
    "dark": dict(bg="#1f1e24", panel="#18171d", border="#3a383f", text="#ececef", muted="#bfbfc3", accent="#9aa8f7",
                 snake="#fc6d26", head="#ffc2a1", levels=["#28272d", "#2f2a6b", "#5565d8", "#7d8ff0", "#d2dcff"]),
    "light": dict(bg="#fbfafd", panel="#ffffff", border="#dcdcde", text="#28272d", muted="#626168", accent="#4b4ba3",
                  snake="#e24329", head="#8a2a0f", levels=["#ececef", "#d2dcff", "#97acff", "#5565d8", "#2f2a6b"]),
}

YEAR_QUERY = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
contributionsCollection(from:$from,to:$to){totalCommitContributions totalPullRequestContributions
totalPullRequestReviewContributions totalIssueContributions totalRepositoryContributions restrictedContributionsCount
contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

STARS_QUERY = """query($login:String!,$after:String){user(login:$login){repositories(first:100,after:$after,
ownerAffiliations:OWNER,isFork:false){pageInfo{hasNextPage endCursor}nodes{stargazerCount}}}}"""


def gql(query: str, **variables) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]


def search_count(kind: str, query: str) -> int | None:
    """total_count from a REST search (kind = "commits" or "issues"); None on failure.

    The per-type fields of GraphQL's contributionsCollection come back as 0 under the workflow's
    bot token, but the search API returns real all-time public totals for any authenticated token.
    """
    url = f"https://api.github.com/search/{kind}?q={urllib.parse.quote(query)}&per_page=1"
    req = urllib.request.Request(url, headers={
        "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-activity-card"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r).get("total_count")
    except Exception as e:  # noqa: BLE001 — never let an optional stat break the activity graph
        print(f"search {kind} ({query}) failed: {e}", file=sys.stderr)
        return None


def fetch(login: str) -> dict:
    created = dt.datetime.fromisoformat(
        gql("query($l:String!){user(login:$l){createdAt}}", l=login)["user"]["createdAt"].replace("Z", "+00:00"))
    today = dt.datetime.now(dt.timezone.utc)

    # Contribution calendar per year (public), for the graph, the all-time contribution total and streaks.
    years, contributions, cc_commits = [], 0, 0
    for year in range(created.year, today.year + 1):
        start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
        end = min(today, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
        c = gql(YEAR_QUERY, login=login, **{"from": start.isoformat(), "to": end.isoformat()})["user"]["contributionsCollection"]
        days = {d["date"]: d["contributionCount"] for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]}
        years.append(dict(year=year, total=c["contributionCalendar"]["totalContributions"], days=days))
        contributions += c["contributionCalendar"]["totalContributions"]
        cc_commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]  # fallback only

    # Owned public, non-fork repositories and the stars they have earned.
    repos = stars = 0
    after = None
    while True:
        page = gql(STARS_QUERY, login=login, after=after)["user"]["repositories"]
        repos += len(page["nodes"])
        stars += sum(n["stargazerCount"] for n in page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    # All-time public commits, PRs, reviews and issues via the search API.
    counts = {}
    for key, (kind, query) in {
        "commits": ("commits", f"author:{login}"),
        "prs": ("issues", f"type:pr author:{login}"),
        "reviews": ("issues", f"type:pr reviewed-by:{login}"),
        "issues": ("issues", f"type:issue author:{login}"),
    }.items():
        counts[key] = search_count(kind, query)
        time.sleep(2)  # stay clear of the search API's secondary rate limit

    totals = dict(contributions=contributions, commits=counts["commits"] if counts["commits"] is not None else cc_commits,
                  prs=counts["prs"] or 0, reviews=counts["reviews"] or 0, issues=counts["issues"] or 0,
                  repos=repos, stars=stars)
    return dict(created=created.date().isoformat(), today=today.date().isoformat(), years=years, totals=totals)


def streaks(years: list[dict]) -> tuple[int, int]:
    days = sorted((d, n) for y in years for d, n in y["days"].items())
    longest = run = 0
    for _, n in days:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current = 0
    for i, (_, n) in enumerate(reversed(days)):
        if n:
            current += 1
        elif i:  # today may not have contributions yet
            break
    return longest, current


THRESHOLDS = [1, 2, 3]  # set per render from the quartiles of active days, like GitHub/GitLab shading


def set_thresholds(counts: list[int]) -> None:
    active = sorted(n for n in counts if n > 0) or [1]
    THRESHOLDS[:] = [active[int(len(active) * q)] for q in (0.25, 0.5, 0.75)]


def level(n: int, peak: int = 0) -> int:
    if n <= 0:
        return 0
    return 1 + sum(n > th for th in THRESHOLDS)


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def snake(cells: list, cell: int, gap: int, t: dict, meta: dict | None = None) -> list[str]:
    """A snake that crawls cell by cell through the whole history, eating every contribution day
    oldest-to-newest and growing as it eats. Pure SMIL, so it animates inside a README <img>."""
    peak = max([c[3] for c in cells] + [1])
    food = sorted((c for c in cells if c[3] > 0), key=lambda c: c[0])
    h, step = cell / 2, cell + gap
    out, empty = [], t["levels"][0]
    if not food:
        return [f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{empty}"><title>{d}: 0</title></rect>'
                for d, x, y, _ in cells]
    # Orthogonal route between food cells along the grid (vertical first, then horizontal, like a snake game).
    first = food[0]
    pts = [(first[1] + h - 4 * step, first[2] + h)]
    for _, x, y, _ in food:
        px, py = pts[-1]
        tx, ty = x + h, y + h
        if py != ty and px != tx:
            pts.append((px, ty))
        pts.append((tx, ty))
    lengths = [abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(lengths) or 1
    speed = max(120.0, total / 55)          # whole history in at most ~55 s
    move = total / speed
    dur = move + 4                          # board stays eaten for a moment, then refills and the loop restarts
    if meta is not None:
        meta.update(pts=pts, speed=speed, move=move, dur=dur)
    at, run, fi = {}, 0.0, 0
    for p, seg in zip(pts[1:], lengths):
        run += seg
        while fi < len(food) and (food[fi][1] + h, food[fi][2] + h) == p:
            at[food[fi][0]] = run / speed
            fi += 1
    for d, x, y, n in cells:
        fill = t["levels"][level(n, peak)]
        anim = ""
        if d in at:
            k = at[d] / dur
            anim = (f'<animate attributeName="fill" dur="{dur:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                    f'values="{fill};{empty};{fill}" keyTimes="0;{k:.4f};{(dur - 0.6) / dur:.4f}"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{fill}"><title>{d}: {n}</title>{anim}</rect>')
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path id="snake-path" d="{path}" fill="none"/>')
    eat_times = sorted(at.values())
    segments, base = 14, 4                  # starts 4 long, grows to 14 as it eats through the history
    for k in reversed(range(segments)):
        lag = k * step * 0.95 / speed
        size = cell + 2 if k == 0 else cell - min(k, 6) * 0.35
        colour = t["head"] if k == 0 else t["snake"]
        op = 1 - k * 0.045
        appear = ""
        if k >= base:
            idx = int((k - base + 1) / (segments - base) * (len(eat_times) - 1))
            show = (eat_times[idx] + lag) / dur
            appear = (f'<animate attributeName="opacity" dur="{dur:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                      f'values="0;{op:.2f};0" keyTimes="0;{min(show, 0.98):.4f};{(dur - 0.6) / dur:.4f}"/>')
        start = lag / dur
        end = min((move + lag) / dur, 0.999)
        out.append(f'<rect class="snake" x="{-size / 2:.1f}" y="{-size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" rx="{3.5 if k == 0 else 2.5}" '
                   f'fill="{colour}" opacity="{0 if appear else op:.2f}">{appear}'
                   f'<animateMotion dur="{dur:.2f}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" '
                   f'keyTimes="0;{start:.4f};{end:.4f};1"><mpath href="#snake-path"/></animateMotion></rect>')
    return out


def head_x(pts: list, dist: float) -> float:
    for a, b in zip(pts, pts[1:]):
        seg = abs(b[0] - a[0]) + abs(b[1] - a[1])
        if dist <= seg:
            return a[0] + (b[0] - a[0]) * (dist / seg if seg else 0)
        dist -= seg
    return pts[-1][0]


def render(data: dict, theme: str) -> str:
    """GitLab-style single activity strip. The calendar holds the whole history since joining; the visible
    one-year window pans along with the snake from the first day to today, then rewinds."""
    t = THEMES[theme]
    days = {d: n for y in data["years"] for d, n in y["days"].items()}
    set_thresholds(list(days.values()))
    first = dt.date.fromisoformat(data["created"])
    last = dt.date.fromisoformat(data["today"])
    start = first - dt.timedelta(days=first.weekday())  # Monday-first rows, like GitLab
    weeks = (last - start).days // 7 + 1
    cell, gap, lw, view = 13, 3, 30, 53
    step = cell + gap
    gx, top = 24 + lw, 70                               # grid left edge, month-label baseline
    gy = top + 12
    width = gx + view * step + 22
    shown = min(weeks, view)
    content = weeks * step
    min_tx = -(content - shown * step)                  # translate that shows the latest year

    cells, d = [], first
    while d <= last:
        cells.append((d.isoformat(), gx + ((d - start).days // 7) * step, gy + d.weekday() * step, days.get(d.isoformat(), 0)))
        d += dt.timedelta(days=1)
    labels, m = [], dt.date(first.year + (first.month == 12), first.month % 12 + 1, 1)
    while m <= last:
        x = gx + ((m - start).days // 7) * step
        jan = m.month == 1
        labels.append(f'<text x="{x}" y="{top}" class="{"my" if jan else "m"}">{MONTHS[m.month - 1]}{f" {m.year}" if jan else ""}</text>')
        m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    meta: dict = {}
    body = snake(cells, cell, gap, t, meta)

    pan = ""
    if meta and min_tx < 0:
        pts, speed, move, dur = meta["pts"], meta["speed"], meta["move"], meta["dur"]
        samples, vals, keys = 240, [], []
        for i in range(samples + 1):
            tt = move * i / samples
            hx = head_x(pts, tt * speed)
            tx = min(0.0, max(min_tx, gx + shown * step * 0.62 - hx))
            vals.append(f"{tx:.1f},0")
            keys.append(f"{tt / dur:.4f}")
        vals += [vals[-1], f"{min(0.0, max(min_tx, gx + shown * step * 0.62 - pts[0][0])):.1f},0"]
        keys += [f"{(dur - 0.9) / dur:.4f}", "1"]
        pan = (f'<animateTransform attributeName="transform" type="translate" dur="{dur:.2f}s" repeatCount="indefinite" '
               f'calcMode="linear" values="{";".join(vals)}" keyTimes="{";".join(keys)}"/>')

    since = first.strftime("%b %Y")
    tot = data["totals"]
    longest, current = streaks(data["years"])
    height = gy + 7 * step + 58
    clip_x, clip_w = gx - 4, shown * step + 6
    wd = "".join(f'<text x="{gx - 10}" y="{gy + r * step + cell - 2}" class="wd">{w}</text>'
                 for r, w in ((0, "M"), (2, "W"), (4, "F"), (6, "S")))
    legend = "".join(f'<rect x="{gx - 4 + i * (cell + 3)}" y="{height - 34}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
                     for i, c in enumerate(t["levels"]))
    fade = (f'<rect x="{clip_x}" y="{top - 14}" width="26" height="{7 * step + 30}" fill="url(#fl)"/>'
            f'<rect x="{clip_x + clip_w - 26}" y="{top - 14}" width="26" height="{7 * step + 30}" fill="url(#fr)"/>')
    title = f"Activity · {since} – today"
    summary = (f"{tot['contributions']:,} contributions · {tot['commits']:,} commits · {tot['repos']:,} repositories · "
               f"longest streak {longest} days")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}: {summary}">
<title>{title}</title>
<style>
.tt{{font:700 20px {FONT};fill:{t['text']}}} .st{{font:400 12.5px {FONT};fill:{t['muted']};text-anchor:end}}
.m{{font:400 12.5px {FONT};fill:{t['muted']}}} .my{{font:700 12.5px {FONT};fill:{t['text']}}}
.wd{{font:400 12.5px {FONT};fill:{t['muted']};text-anchor:end}} .lg{{font:400 12.5px {FONT};fill:{t['muted']};text-anchor:end}}
@media (prefers-reduced-motion:reduce){{.snake{{display:none}}}}
</style>
<defs>
<clipPath id="win"><rect x="{clip_x}" y="{top - 16}" width="{clip_w}" height="{7 * step + 34}"/></clipPath>
<linearGradient id="fl"><stop offset="0" stop-color="{t['panel']}"/><stop offset="1" stop-color="{t['panel']}" stop-opacity="0"/></linearGradient>
<linearGradient id="fr"><stop offset="0" stop-color="{t['panel']}" stop-opacity="0"/><stop offset="1" stop-color="{t['panel']}"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="24" y="36" class="tt">Activity</text>
<text x="{width - 22}" y="35" class="st">since {since} · {summary}</text>
{wd}
<g clip-path="url(#win)"><g transform="translate({min_tx:.1f},0)">{pan}{''.join(labels)}{''.join(body)}</g></g>
{fade}
{legend}
<text x="{width - 22}" y="{height - 23}" class="lg">Commits, pull requests, issues and reviews (public) · current streak {current} days · updated {data["today"]}</text>
</svg>
"""


def stats_card(data: dict, theme: str) -> str:
    """A self-hosted, all-time GitHub stats card: every total is summed across every year since the
    account was created, so it never shows only the last year (unlike the default stats widgets)."""
    t = THEMES[theme]
    tot = data["totals"]
    longest, current = streaks(data["years"])
    since = dt.date.fromisoformat(data["created"]).strftime("%b %Y")
    width, pad, height = 840, 24, 170
    tiles = [
        (f"{tot['contributions']:,}", "contributions"),
        (f"{tot['commits']:,}", "commits"),
        (f"{tot['prs']:,}", "pull requests"),
        (f"{tot['reviews']:,}", "reviews"),
        (f"{tot['issues']:,}", "issues"),
        (f"{tot['repos']:,}", "repositories"),
    ]
    inner = width - 2 * pad
    colw = inner / len(tiles)
    body = []
    for i, (value, label) in enumerate(tiles):
        cx = pad + colw * i + colw / 2
        if i:
            dx = pad + colw * i
            body.append(f'<line x1="{dx:.1f}" y1="74" x2="{dx:.1f}" y2="126" stroke="{t["border"]}"/>')
        body.append(f'<text x="{cx:.1f}" y="102" class="v" style="animation-delay:{i * 0.08:.2f}s">{value}</text>'
                     f'<text x="{cx:.1f}" y="124" class="l">{label}</text>')
    foot = (f"Longest streak {longest} days · current streak {current} days · "
            f"{tot['stars']:,} stars earned · public contributions · updated {data['today']}")
    aria = f"All-time GitHub stats since {since}: " + ", ".join(f"{v} {l}" for v, l in tiles)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">
<title>GitHub activity — all time</title>
<style>
.tt{{font:700 20px {FONT};fill:{t['text']}}} .st{{font:400 12.5px {FONT};fill:{t['muted']};text-anchor:end}}
.v{{font:700 26px {FONT};fill:{t['accent']};text-anchor:middle;transform-box:fill-box;transform-origin:center;animation:pop .8s cubic-bezier(.2,.7,.2,1) both}}
.l{{font:400 12.5px {FONT};fill:{t['muted']};text-anchor:middle}} .ft{{font:400 12px {FONT};fill:{t['muted']}}}
@keyframes pop{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:translateY(0)}}}}
@media (prefers-reduced-motion:reduce){{.v{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="24" y="36" class="tt">GitHub activity — all time</text>
<text x="{width - 22}" y="35" class="st">since {since}</text>
{''.join(body)}
<text x="24" y="{height - 20}" class="ft">{foot}</text>
</svg>
"""


def main() -> None:
    login, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(Path(os.environ["ACTIVITY_FIXTURE"]).read_text()) if os.environ.get("ACTIVITY_FIXTURE") else fetch(login)
    for theme in THEMES:
        (out / f"activity-{theme}.svg").write_text(render(data, theme))
        (out / f"stats-{theme}.svg").write_text(stats_card(data, theme))
    print(f"{login}: {data['totals']['contributions']} contributions across {len(data['years'])} years since {data['created']}")


if __name__ == "__main__":
    main()
