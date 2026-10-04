#!/usr/bin/env python3
"""Generate assets/activity.svg, an "activity at a glance" card built from the GitHub GraphQL API:
weekday pattern, monthly volume, active weeks and top languages. It deliberately does not
redraw GitHub's own contribution graph. Standard library only.

Env:
  GITHUB_TOKEN  required (the workflow's built-in token is enough for public data)
"""
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config" / "consistency.json").read_text())
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "activity.svg"
EXCLUDE = set(CFG.get("exclude_languages", ["Jupyter Notebook", "HTML", "CSS"]))
TOP_N = 6

QUERY = """query($u:String!){user(login:$u){
  repositories(first:100,ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC){
    nodes{languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
  contributionsCollection{contributionCalendar{totalContributions
    weeks{contributionDays{date contributionCount}}}}
}}"""

FONT = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
SANS = '"Segoe UI",Helvetica,Arial,sans-serif'
BAR, BAR_HI = "#2f81d8", "#79c0ff"
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def fetch(username: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"u": username}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "activity-chart"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]


def languages(user: dict):
    size, color = defaultdict(int), {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name in EXCLUDE:
                continue
            size[name] += e["size"]
            color[name] = e["node"]["color"] or "#8b949e"
    total = sum(size.values()) or 1
    ranked = sorted(size.items(), key=lambda kv: -kv[1])
    top = [(n, s / total * 100, color[n]) for n, s in ranked[:TOP_N]]
    other = sum(s for _, s in ranked[TOP_N:]) / total * 100
    if other >= 0.5:
        top.append(("Other", other, "#6e7681"))
    return top


def rhythm(user: dict):
    cal = user["contributionsCollection"]["contributionCalendar"]
    by_wd, by_month = [0] * 7, defaultdict(int)
    active_weeks = active_days = total = 0
    for w in cal["weeks"]:
        week_sum = 0
        for d in w["contributionDays"]:
            dt, n = date.fromisoformat(d["date"]), d["contributionCount"]
            by_wd[dt.weekday()] += n
            by_month[(dt.year, dt.month)] += n
            week_sum += n
            active_days += n > 0
            total += n
        active_weeks += week_sum > 0
    months = sorted(by_month)[-12:]
    return {"total": cal["totalContributions"], "weeks": len(cal["weeks"]), "active_weeks": active_weeks,
            "active_days": active_days, "by_wd": by_wd,
            "months": [(date(y, m, 1).strftime("%b"), by_month[(y, m)]) for y, m in months]}


def build(user: dict) -> str:
    r = rhythm(user)
    W, H = 960, 612
    top_wd = max(range(7), key=lambda i: r["by_wd"][i])      # first one wins a tie
    busiest = WEEKDAYS[top_wd]
    avg = r["total"] / r["active_days"] if r["active_days"] else 0
    stats = [(f'{r["total"]:,}', "Contributions, last year"),
             (f'{r["active_weeks"]} / {r["weeks"]}', "Weeks with activity"),
             (busiest, "Busiest weekday"),
             (f"{avg:.1f}", "Avg per active day")]
    tiles = "".join(
        f'<rect x="{48 + i*219}" y="100" width="205" height="76" rx="10" class="tile"/>'
        f'<text x="{64 + i*219}" y="138" class="big">{v}</text>'
        f'<text x="{64 + i*219}" y="161" class="lab">{k}</text>'
        for i, (v, k) in enumerate(stats))

    # weekday pattern: horizontal bars
    wmax = max(r["by_wd"]) or 1
    wtot = sum(r["by_wd"]) or 1
    wd = ""
    for i, n in enumerate(r["by_wd"]):
        y = 248 + i * 29
        w = 250 * n / wmax
        col = BAR_HI if i == top_wd else BAR
        wd += (f'<text x="48" y="{y+13}" class="lab2">{WEEKDAYS[i]}</text>'
               f'<rect x="92" y="{y}" width="250" height="18" rx="4" class="track"/>'
               f'<rect x="92" y="{y}" width="{max(w,2):.1f}" height="18" rx="4" fill="{col}" class="grow" '
               f'style="animation-delay:{i*60}ms"/>'
               f'<text x="456" y="{y+13}" text-anchor="end" class="lab">{n} · {n/wtot*100:.0f}%</text>')

    # monthly volume: vertical bars
    mmax = max((n for _, n in r["months"]), default=1) or 1
    mo, base, top = "", 424, 262
    for i, (m, n) in enumerate(r["months"]):
        x = 520 + i * 33
        h = (base - top) * n / mmax
        col = BAR_HI if n == mmax else BAR
        mo += (f'<rect x="{x}" y="{base-max(h,2):.1f}" width="24" height="{max(h,2):.1f}" rx="4" fill="{col}" '
               f'class="rise" style="animation-delay:{i*50}ms"/>'
               f'<text x="{x+12}" y="{base-max(h,2)-6:.1f}" text-anchor="middle" class="axis">{n}</text>'
               f'<text x="{x+12}" y="{base+18}" text-anchor="middle" class="axis">{m}</text>')

    # languages
    langs = languages(user)
    ty = 478
    bar, x = "", 48.0
    for n, p, c in langs:
        w = 864 * p / 100
        bar += f'<rect x="{x:.1f}" y="{ty+14}" width="{max(w-2,1):.1f}" height="10" fill="{c}"/>'
        x += w
    items = "".join(
        f'<circle cx="{54 + (i%4)*216}" cy="{ty+48 + (i//4)*26}" r="5" fill="{c}"/>'
        f'<text x="{68 + (i%4)*216}" y="{ty+52 + (i//4)*26}" class="lab2">{n}</text>'
        f'<text x="{228 + (i%4)*216}" y="{ty+52 + (i//4)*26}" text-anchor="end" class="lab">{p:.1f}%</text>'
        for i, (n, p, c) in enumerate(langs))
    today = datetime.now(timezone.utc).date().isoformat()

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">Activity at a glance: contributions by weekday, contributions per month, active weeks and top languages</title>
  <style>
    .bg{{fill:#0d1117}} .card{{fill:#11161d;stroke:#30363d}} .tile{{fill:#161b22;stroke:#21262d}} .track{{fill:#161b22}}
    .h{{font:700 22px {SANS};fill:#e6edf3}} .s{{font:13px {FONT};fill:#8b949e}}
    .big{{font:700 28px {SANS};fill:#e6edf3}} .lab{{font:12px {SANS};fill:#8b949e}}
    .lab2{{font:13px {SANS};fill:#e6edf3}} .axis{{font:11px {FONT};fill:#7d8590}}
    .sec{{font:600 11px {FONT};fill:#8b949e;letter-spacing:2px}}
    .grow{{transform-box:fill-box;transform-origin:left center;animation:grow .7s ease-out both}}
    .rise{{transform-box:fill-box;transform-origin:center bottom;animation:rise .7s ease-out both}}
    @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
    @keyframes rise{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
    @media (prefers-reduced-motion:reduce){{.grow,.rise{{animation:none}}}}
  </style>
  <rect class="bg" width="{W}" height="{H}" rx="18"/>
  <rect class="card" x="20" y="20" width="920" height="{H-40}" rx="14"/>
  <text x="48" y="62" class="h">Activity at a glance</text>
  <text x="48" y="84" class="s">last 12 months · live from the GitHub API · refreshed daily</text>
  {tiles}
  <text x="48" y="222" class="sec">CONTRIBUTIONS BY WEEKDAY</text>
  {wd}
  <text x="520" y="222" class="sec">CONTRIBUTIONS PER MONTH</text>
  {mo}
  <text x="48" y="{ty}" class="sec">TOP LANGUAGES · PUBLIC REPOSITORIES</text>
  {bar}{items}
  <text x="912" y="{H-34}" text-anchor="end" class="s">updated {today} UTC</text>
</svg>
'''


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is required")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(fetch(CFG["username"], token)), encoding="utf-8")
    print(f"wrote {OUT}")
