#!/usr/bin/env python3
"""Generate assets/consistency.svg: the 1% compounding curve, today's position on it,
and live GitHub contribution streaks. Standard library only.

Env:
  GITHUB_TOKEN  optional; enables the contribution-streak panel (GraphQL API)
  TODAY         optional YYYY-MM-DD override for testing
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config" / "consistency.json").read_text())
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "consistency.svg"

W, H = 960, 440
PX0, PX1, PY0, PY1 = 76, 600, 120, 350      # plot box
YMAX = 40.0
CYCLE = 365


def today_utc() -> date:
    t = os.environ.get("TODAY")
    return date.fromisoformat(t) if t else datetime.now(timezone.utc).date()


def fetch_streaks(username: str, token: str, today: date):
    """Return (current_streak, longest_streak, active_days) over the last year, or None."""
    query = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
      weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"u": username}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "consistency-chart"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    except Exception as exc:                      # degrade gracefully, never fail the workflow
        print(f"streak lookup skipped: {exc}", file=sys.stderr)
        return None
    counts = {d["date"]: d["contributionCount"] for w in weeks for d in w["contributionDays"]}
    days = sorted(k for k in counts if k <= today.isoformat())
    active = sum(1 for k in days if counts[k] > 0)
    longest = run = 0
    for k in days:
        run = run + 1 if counts[k] > 0 else 0
        longest = max(longest, run)
    cur, d = 0, today
    if counts.get(d.isoformat(), 0) == 0:         # today may not have a contribution yet
        d -= timedelta(days=1)
    while counts.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= timedelta(days=1)
    return cur, longest, active


def sx(d): return PX0 + (PX1 - PX0) * d / CYCLE
def sy(v): return PY1 - (PY1 - PY0) * min(v, YMAX) / YMAX


def curve(rate: float) -> str:
    pts = [(d, (1 + rate) ** d) for d in range(0, CYCLE + 1, 5)]
    if pts[-1][0] != CYCLE:
        pts.append((CYCLE, (1 + rate) ** CYCLE))
    return "M" + " L".join(f"{sx(d):.1f},{sy(v):.1f}" for d, v in pts)


def build() -> str:
    gain = float(CFG["daily_gain"])
    start = date.fromisoformat(CFG["start_date"])
    today = today_utc()
    day = max((today - start).days + 1, 1)
    cd = (day - 1) % CYCLE + 1                    # day within the current 365-day cycle
    year = (day - 1) // CYCLE + 1
    value = (1 + gain) ** cd
    streaks = None
    if os.environ.get("GITHUB_TOKEN"):
        streaks = fetch_streaks(CFG["username"], os.environ["GITHUB_TOKEN"], today)

    stamp = (os.environ["TODAY"] + " 00:00") if os.environ.get("TODAY") else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    mx, my = sx(cd), sy(value)
    anchor, lx = ("end", mx - 12) if mx > 380 else ("start", mx + 12)

    grid = "".join(
        f'<line x1="{PX0}" y1="{sy(v):.1f}" x2="{PX1}" y2="{sy(v):.1f}" class="grid"/>'
        f'<text x="{PX0-10}" y="{sy(v)+4:.1f}" text-anchor="end" class="axis">{int(v)}×</text>'
        for v in (0, 10, 20, 30, 40))
    xt = "".join(
        f'<text x="{sx(d):.1f}" y="{PY1+22}" text-anchor="middle" class="axis">{d}d</text>'
        for d in (0, 90, 180, 270, 365))
    miles = ""
    for d in (30, 90, 180, 365):
        v = (1 + gain) ** d
        a, off = ("end", -10) if d == 365 else ("start", 8)
        miles += f'<circle cx="{sx(d):.1f}" cy="{sy(v):.1f}" r="3.5" fill="#0d1117" stroke="#58a6ff" stroke-width="2"/>'
        if abs(d - cd) > 60:                      # skip labels that would sit under the "today" label
            miles += (f'<text x="{sx(d)+off:.1f}" y="{sy(v)-10:.1f}" text-anchor="{a}" class="mile">'
                      f'{d}d · {v:.2f}×</text>')

    if streaks:
        cur, longest, active = streaks
        rows = [("Current streak", f"{cur} days"), ("Longest streak", f"{longest} days"),
                ("Active days, last year", f"{active}")]
    else:
        rows = [("Refreshed", "daily"), ("Source", "GitHub Actions")]
    panel = "".join(
        f'<text x="648" y="{262 + i*34}" class="plabel">{k}</text>'
        f'<text x="912" y="{262 + i*34}" text-anchor="end" class="pval">{v}</text>'
        f'<line x1="648" y1="{272 + i*34}" x2="912" y2="{272 + i*34}" class="grid"/>'
        for i, (k, v) in enumerate(rows))
    cycle_txt = f"Year {year} · Day {cd}" if year > 1 else f"Day {cd}"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Consistency compounds</title>
  <desc id="d">{cycle_txt}: improving 1% a day gives {value:.2f} times the starting level; after 365 days it is about 37.8 times.</desc>
  <style>
    .bg{{fill:#0d1117}} .card{{fill:#11161d;stroke:#30363d}}
    .h{{font:700 22px "Segoe UI",Helvetica,Arial,sans-serif;fill:#e6edf3}}
    .s{{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e}}
    .axis{{font:11px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#7d8590}}
    .mile{{font:11px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#58a6ff}}
    .grid{{stroke:#21262d;stroke-width:1}}
    .lg{{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e}}
    .big{{font:700 40px "Segoe UI",Helvetica,Arial,sans-serif;fill:#e6edf3}}
    .val{{font:700 28px "Segoe UI",Helvetica,Arial,sans-serif;fill:#58a6ff}}
    .plabel{{font:13px "Segoe UI",Helvetica,Arial,sans-serif;fill:#8b949e}}
    .pval{{font:700 14px "Segoe UI",Helvetica,Arial,sans-serif;fill:#e6edf3}}
    .draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s ease-out forwards}}
    .halo{{transform-box:fill-box;transform-origin:center;animation:halo 2s ease-out infinite}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    @keyframes halo{{0%{{opacity:.9;transform:scale(1)}}100%{{opacity:0;transform:scale(3.2)}}}}
    @media (prefers-reduced-motion:reduce){{.draw{{animation:none;stroke-dashoffset:0}}.halo{{animation:none;opacity:0}}}}
  </style>
  <rect class="bg" width="{W}" height="{H}" rx="18"/>
  <rect class="card" x="20" y="20" width="920" height="400" rx="14"/>
  <text x="48" y="62" class="h">Consistency compounds</text>
  <text x="48" y="86" class="s">1% better every day · 1.01^365 ≈ 37.8×</text>
  {grid}{xt}
  <path d="{curve(-gain)}" fill="none" stroke="#f85149" stroke-width="2" opacity=".75" pathLength="1" class="draw"/>
  <path d="{curve(0)}" fill="none" stroke="#6e7681" stroke-width="2" stroke-dasharray="none" opacity=".9"/>
  <path d="{curve(gain)}" fill="none" stroke="#58a6ff" stroke-width="3" pathLength="1" class="draw"/>
  {miles}
  <circle cx="{mx:.1f}" cy="{my:.1f}" r="5" class="halo" fill="#58a6ff"/>
  <circle cx="{mx:.1f}" cy="{my:.1f}" r="6" fill="#e6edf3" stroke="#58a6ff" stroke-width="2.5"/>
  <text x="{lx:.1f}" y="{my-14:.1f}" text-anchor="{anchor}" class="pval">{cycle_txt}</text>
  <g transform="translate(76,404)">
    <line x1="0" y1="-4" x2="22" y2="-4" stroke="#58a6ff" stroke-width="3"/><text x="30" class="lg">+1% daily</text>
    <line x1="130" y1="-4" x2="152" y2="-4" stroke="#6e7681" stroke-width="2"/><text x="160" class="lg">no change</text>
    <line x1="250" y1="-4" x2="272" y2="-4" stroke="#f85149" stroke-width="2"/><text x="280" class="lg">−1% daily</text>
  </g>
  <line x1="628" y1="50" x2="628" y2="396" class="grid"/>
  <text x="648" y="104" class="plabel">TODAY</text>
  <text x="648" y="150" class="big">{cycle_txt}</text>
  <text x="648" y="188" class="val">{value:.2f}×</text>
  <text x="648" y="212" class="s">since {start.isoformat()}</text>
  {panel}
  <text x="912" y="404" text-anchor="end" class="s">updated {stamp} UTC</text>
</svg>
'''


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT}")
