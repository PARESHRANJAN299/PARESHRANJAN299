#!/usr/bin/env python3
"""Generate assets/activity.svg: contribution heatmap, headline stats and top languages,
all pulled live from the GitHub GraphQL API. Standard library only.

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
EXCLUDE = set(CFG.get("exclude_languages", ["Jupyter Notebook"]))
TOP_N = 6

QUERY = """query($u:String!){user(login:$u){
  repositories(first:100,ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC){totalCount
    nodes{languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
  pullRequests{totalCount}
  contributionsCollection{totalCommitContributions
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}
}}"""
LEVEL = {"NONE": "#161b22", "FIRST_QUARTILE": "#12304f", "SECOND_QUARTILE": "#1b5a9c",
         "THIRD_QUARTILE": "#2f81d8", "FOURTH_QUARTILE": "#79c0ff"}

FONT = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
SANS = '"Segoe UI",Helvetica,Arial,sans-serif'


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


def build(user: dict) -> str:
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    stats = [
        (f'{cal["totalContributions"]:,}', "Contributions, last year"),
        (f'{user["contributionsCollection"]["totalCommitContributions"]:,}', "Commits"),
        (f'{user["pullRequests"]["totalCount"]:,}', "Pull requests"),
        (f'{user["repositories"]["totalCount"]:,}', "Public repositories"),
    ]
    W, H = 960, 520
    tiles = "".join(
        f'<rect x="{48 + i*219}" y="92" width="205" height="76" rx="10" class="tile"/>'
        f'<text x="{64 + i*219}" y="130" class="big">{v}</text>'
        f'<text x="{64 + i*219}" y="153" class="lab">{k}</text>'
        for i, (v, k) in enumerate(stats))

    # heatmap
    X0, Y0, CELL, GAP = 74, 226, 12, 3
    cells, months, last_m = [], [], None
    for wi, w in enumerate(weeks):
        days = w["contributionDays"]
        m = date.fromisoformat(days[0]["date"]).strftime("%b")
        if m != last_m and wi < len(weeks) - 2:
            months.append(f'<text x="{X0 + wi*(CELL+GAP)}" y="{Y0-10}" class="axis">{m}</text>')
            last_m = m
        for d in days:
            wd = date.fromisoformat(d["date"]).isoweekday() % 7      # Sunday = 0
            cells.append(
                f'<rect x="{X0 + wi*(CELL+GAP)}" y="{Y0 + wd*(CELL+GAP)}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{LEVEL.get(d["contributionLevel"], LEVEL["NONE"])}" class="c" style="animation-delay:{wi*18}ms">'
                f'<title>{d["contributionCount"]} on {d["date"]}</title></rect>')
    dow = "".join(f'<text x="{X0-10}" y="{Y0 + i*(CELL+GAP) + 10}" text-anchor="end" class="axis">{n}</text>'
                  for i, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    ly = Y0 + 7 * (CELL + GAP) + 18
    legend = (f'<text x="{X0}" y="{ly}" class="lab">Less</text>' +
              "".join(f'<rect x="{X0 + 34 + i*17}" y="{ly-10}" width="12" height="12" rx="2.5" fill="{c}"/>'
                      for i, c in enumerate(LEVEL.values())) +
              f'<text x="{X0 + 34 + 5*17 + 4}" y="{ly}" class="lab">More</text>')

    # languages
    langs = languages(user)
    ty = ly + 44
    bar, x = "", 48.0
    for i, (n, p, c) in enumerate(langs):
        w = 864 * p / 100
        bar += f'<rect x="{x:.1f}" y="{ty+14}" width="{max(w-2,1):.1f}" height="10" fill="{c}"/>'
        x += w
    items = "".join(
        f'<circle cx="{54 + (i%3)*288}" cy="{ty+52 + (i//3)*26}" r="5" fill="{c}"/>'
        f'<text x="{68 + (i%3)*288}" y="{ty+56 + (i//3)*26}" class="lab2">{n}</text>'
        f'<text x="{300 + (i%3)*288}" y="{ty+56 + (i//3)*26}" text-anchor="end" class="lab">{p:.1f}%</text>'
        for i, (n, p, c) in enumerate(langs))
    today = datetime.now(timezone.utc).date().isoformat()

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">GitHub activity: contributions over the last year, headline stats and top languages</title>
  <style>
    .bg{{fill:#0d1117}} .card{{fill:#11161d;stroke:#30363d}} .tile{{fill:#161b22;stroke:#21262d}}
    .h{{font:700 22px {SANS};fill:#e6edf3}} .s{{font:13px {FONT};fill:#8b949e}}
    .big{{font:700 28px {SANS};fill:#e6edf3}} .lab{{font:12px {SANS};fill:#8b949e}}
    .lab2{{font:13px {SANS};fill:#e6edf3}} .axis{{font:11px {FONT};fill:#7d8590}}
    .sec{{font:600 11px {FONT};fill:#8b949e;letter-spacing:2px}}
    .c{{animation:fade .5s ease-out both}} @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
    @media (prefers-reduced-motion:reduce){{.c{{animation:none}}}}
  </style>
  <rect class="bg" width="{W}" height="{H}" rx="18"/>
  <rect class="card" x="20" y="20" width="920" height="{H-40}" rx="14"/>
  <text x="48" y="62" class="h">GitHub activity</text>
  {tiles}
  <text x="48" y="{Y0-34}" class="sec">CONTRIBUTIONS · LAST 12 MONTHS</text>
  {"".join(months)}{dow}{"".join(cells)}{legend}
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
