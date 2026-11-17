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
    created = dt.datetime.fromisoformat(
        gql("query($l:String!){user(login:$l){createdAt}}", l=login)["user"]["createdAt"].replace("Z", "+00:00"))
    today = dt.datetime.now(dt.timezone.utc)
    years, totals = [], dict(contributions=0, commits=0, prs=0, reviews=0, issues=0, repos=0)
    for year in range(created.year, today.year + 1):
        start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
        end = min(today, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
        c = gql(YEAR_QUERY, login=login, **{"from": start.isoformat(), "to": end.isoformat()})["user"]["contributionsCollection"]
        days = {d["date"]: d["contributionCount"] for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]}
        years.append(dict(year=year, total=c["contributionCalendar"]["totalContributions"], days=days))
        totals["contributions"] += c["contributionCalendar"]["totalContributions"]
        totals["commits"] += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        totals["prs"] += c["totalPullRequestContributions"]
        totals["reviews"] += c["totalPullRequestReviewContributions"]
        totals["issues"] += c["totalIssueContributions"]
        totals["repos"] += c["totalRepositoryContributions"]
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


def snake(cells: list, cell: int, gap: int, t: dict) -> list[str]:
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
    speed = max(140.0, total / 50)          # whole history in at most ~50 s
    move = total / speed
    dur = move + 4                          # board stays eaten for a moment, then refills and the loop restarts
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


def render(data: dict, theme: str) -> str:
    t = THEMES[theme]
    days = {d: n for y in data["years"] for d, n in y["days"].items()}
    set_thresholds(list(days.values()))
    first = dt.date.fromisoformat(data["created"])
    last = dt.date.fromisoformat(data["today"])
    start = first - dt.timedelta(days=first.weekday())  # Monday on/before the first day (GitLab rows start on Monday)
    weeks = (last - start).days // 7 + 1
    cell, gap, lw = 12, 3, 34
    step = cell + gap
    per_line = 56                                                    # ≈ 13 months per strip, like GitLab
    lines = -(-weeks // per_line)
    width = 24 + lw + per_line * step + 24
    longest, current = streaks(data["years"])
    since = first.strftime("%b %Y")
    tot = data["totals"]
    tiles = [(f"{tot['contributions']:,}", "contributions"), (f"{tot['commits']:,}", "commits"),
             (f"{tot['prs']:,}", "pull requests"), (f"{tot['repos']:,}", "repositories created"),
             (f"{len(data['years'])}", "years on GitHub"), (f"{longest}", "longest streak (days)")]
    out, top = [], 78
    tw = (width - 48 - 5 * 10) / 6
    for i, (value, label) in enumerate(tiles):
        x = 24 + i * (tw + 10)
        out.append(f'<g class="f" style="animation-delay:{i * 0.08:.2f}s"><rect x="{x:.1f}" y="{top}" width="{tw:.1f}" height="58" rx="10" '
                   f'fill="{t["bg"]}" stroke="{t["border"]}"/><text x="{x + tw / 2:.1f}" y="{top + 27}" class="v">{value}</text>'
                   f'<text x="{x + tw / 2:.1f}" y="{top + 46}" class="l">{label}</text></g>')

    # continuous calendar: one column per week from the first day to today, wrapped into lines
    y0, line_h = top + 58 + 44, 7 * step + 34
    cells = []
    d = first
    while d <= last:
        w = (d - start).days // 7
        line, col = divmod(w, per_line)
        x = 24 + lw + col * step
        y = y0 + line * line_h + d.weekday() * step
        cells.append((d.isoformat(), x, y, days.get(d.isoformat(), 0)))
        d += dt.timedelta(days=1)
    for line in range(lines):  # month labels on every line; the year is shown on January (and on the very first month)
        labels = []
        for w in range(line * per_line, min((line + 1) * per_line, weeks)):
            for i in range(7):
                day = start + dt.timedelta(weeks=w, days=i)
                if day.day == 1 and first <= day <= last:
                    yearly = day.month == 1 or not (labels or line)
                    text = f"{MONTHS[day.month - 1]} {day.year}" if yearly else MONTHS[day.month - 1]
                    labels.append([24 + lw + (w - line * per_line) * step, text, yearly])
        kept = []
        for lab in labels:  # drop a plain month label that would collide with its neighbour
            if kept and lab[0] < kept[-1][0] + len(kept[-1][1]) * 6.2 + 6:
                if lab[2] and not kept[-1][2]:
                    kept[-1] = lab
                continue
            kept.append(lab)
        kept = [lab for lab in kept if lab[0] + len(lab[1]) * 7 < width - 16]
        for x, text, yearly in kept:
            out.append(f'<text x="{x}" y="{y0 + line * line_h - 8}" class="{"my" if yearly else "m"}">{text}</text>')
        for row, wd in ((0, "M"), (2, "W"), (4, "F"), (6, "S")):
            out.append(f'<text x="{24 + lw - 12}" y="{y0 + line * line_h + row * step + cell - 1.5}" class="wd">{wd}</text>')
    out.extend(snake(cells, cell, gap, t))
    grid_bottom = y0 + lines * line_h - 22

    # month-by-month bars for the whole history
    months, m = [], dt.date(first.year, first.month, 1)
    while m <= last:
        n = sum(v for k, v in days.items() if k.startswith(m.strftime("%Y-%m")))
        months.append((m, n))
        m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    bar_top, bar_h = grid_bottom + 46, 70
    out.append(f'<text x="24" y="{bar_top - 14}" class="sec">Contributions per month</text>')
    bw = (width - 48) / len(months)
    peak_m = max([n for _, n in months] + [1])
    for i, (m, n) in enumerate(months):
        hgt = 0 if n == 0 else max(2, n / peak_m * bar_h)
        x = 24 + i * bw
        out.append(f'<rect x="{x + 0.6:.1f}" y="{bar_top + bar_h - hgt:.1f}" width="{max(bw - 1.2, 1):.1f}" height="{hgt:.1f}" rx="1.5" '
                   f'fill="{t["levels"][3]}" class="b" style="animation-delay:{i * 0.01:.2f}s"><title>{m:%b %Y}: {n}</title></rect>')
        if m.month == 1 or i == 0:
            out.append(f'<line x1="{x:.1f}" y1="{bar_top + bar_h + 2}" x2="{x:.1f}" y2="{bar_top + bar_h + 7}" stroke="{t["muted"]}"/>'
                       f'<text x="{x + 2:.1f}" y="{bar_top + bar_h + 19}" class="m">{m.year}</text>')
    out.append(f'<line x1="24" y1="{bar_top + bar_h + 0.5}" x2="{width - 24}" y2="{bar_top + bar_h + 0.5}" stroke="{t["border"]}"/>')
    height = bar_top + bar_h + 58
    legend = "".join(f'<rect x="{24 + i * (cell + 4)}" y="{height - 30}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
                     for i, c in enumerate(t["levels"]))
    note = (f'<text x="{width - 24}" y="{height - 19.5}" class="lg" text-anchor="end">Commits, pull requests, issues and reviews '
            f'(public) · current streak {current} days · updated {data["today"]}</text>')
    title = f"Activity · {since} – today"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}: {tot['contributions']:,} contributions">
<title>{title}</title>
<style>
.tt{{font:700 18px {FONT};fill:{t['text']}}} .st{{font:400 12.5px {FONT};fill:{t['muted']}}} .sec{{font:600 12.5px {FONT};fill:{t['text']}}}
.v{{font:700 20px {FONT};fill:{t['accent']};text-anchor:middle}} .l{{font:400 11.5px {FONT};fill:{t['muted']};text-anchor:middle}}
.m{{font:400 12px {FONT};fill:{t['muted']}}} .wd{{font:400 12px {FONT};fill:{t['muted']};text-anchor:end}} .my{{font:700 12px {FONT};fill:{t['text']}}} .lg{{font:400 11px {FONT};fill:{t['muted']}}}
.f{{animation:fade .6s ease-out both}} .b{{transform-box:fill-box;transform-origin:bottom;animation:grow .8s ease-out both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}} @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@media (prefers-reduced-motion:reduce){{.f,.b{{animation:none}}.snake{{display:none}}}}
</style>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="24" y="38" class="tt">{title}</text>
<text x="24" y="60" class="st">Full history since joining GitHub · the snake eats every contribution day, oldest first, and grows as it goes</text>
{''.join(out)}
{legend}
{note}
</svg>
"""


def main() -> None:
    login, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(Path(os.environ["ACTIVITY_FIXTURE"]).read_text()) if os.environ.get("ACTIVITY_FIXTURE") else fetch(login)
    for theme in THEMES:
        (out / f"activity-{theme}.svg").write_text(render(data, theme))
    print(f"{login}: {data['totals']['contributions']} contributions across {len(data['years'])} years since {data['created']}")


if __name__ == "__main__":
    main()
