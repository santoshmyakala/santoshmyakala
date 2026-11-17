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
THEMES = {
    "dark": dict(bg="#0d1117", panel="#11161f", border="#30363d", text="#e6edf3", muted="#9da7b3", accent="#58a6ff",
                 levels=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]),
    "light": dict(bg="#ffffff", panel="#f8fafc", border="#d0d7de", text="#1f2328", muted="#57606a", accent="#0969da",
                  levels=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]),
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


def level(n: int, peak: int) -> int:
    if n <= 0:
        return 0
    return min(4, 1 + int(3 * n / max(peak, 1)))


def render(data: dict, theme: str) -> str:
    t = THEMES[theme]
    cell, gap, label_w, total_w = 10, 3, 52, 70
    grid_w = 53 * (cell + gap)
    width = 24 + label_w + grid_w + total_w + 24
    years = list(reversed(data["years"]))  # most recent first
    peak = max([n for y in years for n in y["days"].values()] + [1])
    longest, current = streaks(data["years"])
    since = dt.date.fromisoformat(data["created"]).strftime("%b %Y")
    tot = data["totals"]
    tiles = [(f"{tot['contributions']:,}", "contributions"), (f"{tot['commits']:,}", "commits"),
             (f"{tot['prs']:,}", "pull requests"), (f"{tot['repos']:,}", "repositories created"),
             (f"{len(years)}", "years active"), (f"{longest}", "longest streak (days)")]
    top = 78
    out = []
    tw = (width - 48 - 5 * 10) / 6
    for i, (value, label) in enumerate(tiles):
        x = 24 + i * (tw + 10)
        out.append(f'<g class="f" style="animation-delay:{i * 0.08:.2f}s"><rect x="{x:.1f}" y="{top}" width="{tw:.1f}" height="58" rx="10" '
                   f'fill="{t["bg"]}" stroke="{t["border"]}"/><text x="{x + tw / 2:.1f}" y="{top + 27}" class="v">{value}</text>'
                   f'<text x="{x + tw / 2:.1f}" y="{top + 46}" class="l">{label}</text></g>')
    y0 = top + 58 + 34
    row_h = 7 * (cell + gap) + 18
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m, name in enumerate(months):
        wk = (dt.date(2001, m + 1, 1) - dt.date(2001, 1, 1)).days // 7
        out.append(f'<text x="{24 + label_w + wk * (cell + gap):.1f}" y="{y0 - 8}" class="m">{name}</text>')
    for r, y in enumerate(years):
        yy = y0 + r * row_h
        out.append(f'<text x="24" y="{yy + 3.5 * (cell + gap) + 4:.1f}" class="yr">{y["year"]}</text>')
        out.append(f'<text x="{width - 24}" y="{yy + 3.5 * (cell + gap) + 4:.1f}" class="yt">{y["total"]:,}</text>')
        jan1 = dt.date(y["year"], 1, 1)
        offset = (jan1.weekday() + 1) % 7  # Sunday-first rows like GitHub
        for date, n in y["days"].items():
            d = dt.date.fromisoformat(date)
            if d.year != y["year"]:
                continue
            idx = (d - jan1).days + offset
            x = 24 + label_w + (idx // 7) * (cell + gap)
            cy = yy + (idx % 7) * (cell + gap)
            delay = (r * 53 + idx // 7) * 0.004
            out.append(f'<rect x="{x}" y="{cy}" width="{cell}" height="{cell}" rx="2.5" fill="{t["levels"][level(n, peak)]}" '
                       f'class="c" style="animation-delay:{delay:.3f}s"><title>{date}: {n}</title></rect>')
    height = y0 + len(years) * row_h + 34
    legend_x = width - 24 - 5 * (cell + 3) - 70
    legend = (f'<text x="{legend_x - 6}" y="{height - 16}" class="lg" text-anchor="end">Less</text>'
              + "".join(f'<rect x="{legend_x + i * (cell + 3)}" y="{height - 25}" width="{cell}" height="{cell}" rx="2.5" fill="{c}"/>'
                        for i, c in enumerate(t["levels"]))
              + f'<text x="{legend_x + 5 * (cell + 3) + 4}" y="{height - 16}" class="lg">More</text>')
    note = (f'<text x="24" y="{height - 16}" class="lg">Public contributions since {since} · current streak {current} days · '
            f'updated {data["today"]}</text>')
    title = f"Contribution history · {since} – today"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}: {tot['contributions']:,} contributions">
<title>{title}</title>
<style>
.tt{{font:700 18px {FONT};fill:{t['text']}}} .st{{font:400 12.5px {FONT};fill:{t['muted']}}}
.v{{font:700 20px {FONT};fill:{t['accent']};text-anchor:middle}} .l{{font:400 11.5px {FONT};fill:{t['muted']};text-anchor:middle}}
.yr{{font:600 12px {FONT};fill:{t['text']}}} .yt{{font:600 12px {FONT};fill:{t['muted']};text-anchor:end}}
.m{{font:400 10.5px {FONT};fill:{t['muted']}}} .lg{{font:400 11px {FONT};fill:{t['muted']}}}
.c{{animation:pop .5s ease-out both}} .f{{animation:fade .6s ease-out both}}
@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}} .c{{transform-box:fill-box;transform-origin:center}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.c,.f{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="24" y="38" class="tt">{title}</text>
<text x="24" y="60" class="st">Every year since joining GitHub, most recent first</text>
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
