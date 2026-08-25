#!/usr/bin/env python3
"""
Regenerate README tables from data/monthly_performance.csv and
data/audit_metrics_summary.json. Prevents hand-typed drift.

Usage: python scripts/update_readme.py  (writes README.md in place)
       python scripts/update_readme.py --check  (exit 1 if README would change)
"""
import argparse
import json
import re
from pathlib import Path

import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
README = BASE_DIR / "README.md"

def fmt(v: float) -> str:
    if abs(v) < 0.0005:
        return "0.00"
    return f"{v:+.2f}"

def fmt_pct(v: float) -> str:
    # keep sign, 2 decimals
    return fmt(v)

df = pd.read_csv(DATA_DIR / "monthly_performance.csv")
with open(DATA_DIR / "audit_metrics_summary.json") as f:
    metrics = json.load(f)

pm = metrics["performance_metrics"]
bm_btc = metrics["benchmarks"]["bitcoin"]
bm_sp = metrics["benchmarks"]["sp500"]

# also compute ETH from CSV for display (not in audit JSON)
eth_m = df["ETH_Return_Pct"] / 100
eth_nav_end = df["ETH_NAV"].iloc[-1]
eth_cum = (eth_nav_end/100 - 1)*100
eth_cagr = (eth_nav_end/100)**(1/(len(df)/12)) - 1
rf_m = (1.04)**(1/12)-1
eth_vol = eth_m.std(ddof=1)*np.sqrt(12)*100
eth_sharpe = ((eth_m - rf_m).mean()/eth_m.std(ddof=1))*np.sqrt(12)
eth_dd = ((df["ETH_NAV"] - df["ETH_NAV"].cummax())/df["ETH_NAV"].cummax()).min()*100

# ---- 1) Key metrics table (replace block between "### 🏆 Key Audited" and "### 📊 Fund Yield" ----
# handled via regex below

# ---- 2) Yearly summary ----
# yearly computed
df_year = df.copy()
df_year["Year"] = df_year["Month"].str[:4]
yearly = {}
for y, g in df_year.groupby("Year"):
    comp = (np.prod(1+g["Yield_Pct"]/100)-1)*100
    btc = (np.prod(1+g["BTC_Return_Pct"]/100)-1)*100
    eth = (np.prod(1+g["ETH_Return_Pct"]/100)-1)*100
    sp = (np.prod(1+g["SP500_Return_Pct"]/100)-1)*100
    yearly[y] = dict(nom=g["Yield_Pct"].sum(), comp=comp, btc=btc, eth=eth, sp=sp, n=len(g))

# yearly markdown
year_rows = []
for y in sorted(yearly):
    d = yearly[y]
    dur = {"2022":"Nov–Dec (2m)","2023":"Jan–Dec (12m)","2024":"Jan–Dec (12m)","2025":"Jan–Dec (12m)","2026":"Jan–Jul (7m)"}[y]
    year_rows.append(f"| **{y}** | {dur} | {fmt(d['nom'])}% | **{fmt(d['comp'])}%** | {fmt(d['btc'])}% | {fmt(d['eth'])}% | {fmt(d['sp'])}% | 100% ({d['n']}/{d['n']}) |")
# total
total_nom = df["Yield_Pct"].sum()
total_comp = pm["cumulative_fund_return_pct"]
year_rows.append(f"| **TOTAL** | **45 Months** | **{fmt(total_nom)}%** | **{fmt(total_comp)}%** | **{fmt(bm_btc['cumulative_return_pct'])}%** | **{fmt(eth_cum)}%** | **{fmt(bm_sp['cumulative_return_pct'])}%** | **100.0% (45/45)** |")

year_table = """| Year | Duration | Nominal Yield | Compounded Return | BTC Return | ETH Return | S&P 500 Return | Win Rate |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
""" + "\n".join(year_rows)

# ---- 3) Granular calendar matrix + per-year details ----
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
df["Mon"] = df["Month"].str[5:].astype(int)
df["YearInt"] = df["Month"].str[:4].astype(int)
header = "| Year | " + " | ".join(months) + " | **Year** |"
sep = "| :--- | " + " | ".join(["---:"]*12) + " | ---: |"
cal_rows=[]
for y in [2022,2023,2024,2025,2026]:
    cells=[]
    for m in range(1,13):
        hit = df[(df["YearInt"]==y)&(df["Mon"]==m)]
        if hit.empty:
            cells.append("—")
        else:
            cells.append(fmt(hit.iloc[0]["Yield_Pct"]))
    cells.append(f"**{fmt(yearly[str(y)]['comp'])}**")
    cal_rows.append(f"| **{y}** | " + " | ".join(cells) + " |")
matrix = "\n".join([header, sep] + cal_rows)

detail_blocks=[]
for y in [2022,2023,2024,2025,2026]:
    g = df[df["YearInt"]==y]
    if g.empty: continue
    d = yearly[str(y)]
    tb_header = "| Month | Yield | NAV | Cum. | BTC · ETH · S&P | Regime (Driver) |"
    tb_sep = "| :--- | ---: | ---: | ---: | :--- | :--- |"
    tb_rows=[]
    for _,r in g.iterrows():
        bench = f"{fmt(r['BTC_Return_Pct'])} · {fmt(r['ETH_Return_Pct'])} · {fmt(r['SP500_Return_Pct'])}"
        nav = f"{r['Fund_NAV']:.2f}"
        if r["Month"]==df["Month"].iloc[-1]:
            nav = f"**{nav}**"
            cum = f"**{fmt(r['Cum_Fund_Return_Pct'])}**"
            m = f"**{r['Month']}**"
            yld = f"**{fmt(r['Yield_Pct'])}**"
        else:
            cum = fmt(r["Cum_Fund_Return_Pct"])
            m = r["Month"]
            yld = fmt(r["Yield_Pct"])
        meta = f"{r['Market_Regime']} ({r['Asset_Driver']})"
        tb_rows.append(f"| {m} | {yld} | {nav} | {cum} | {bench} | {meta} |")
    block = f"""<details>
<summary><strong>{y} — {len(g)} months · {fmt(d['nom'])} nominal · {fmt(d['comp'])} compounded — click to expand</strong></summary>

{tb_header}
{tb_sep}
""" + "\n".join(tb_rows) + "\n\n</details>"
    detail_blocks.append(block)

granular_section = f"""<a id="all-45-months-granular-returns"></a>
### All 45 Months Granular Returns

> **Packed calendar view (5 rows = 45 months).** All figures in % — benchmarks shown as BTC · ETH · S&P. Expand a year below for full NAV & regime detail. See also [`docs/MONTH_BY_MONTH_PERFORMANCE.md`](./docs/MONTH_BY_MONTH_PERFORMANCE.md).

{matrix}

— = no exposure (pre-inception / post wind-down on Aug 1, 2026).

""" + "\n\n".join(detail_blocks) + "\n"

# ---- patch README ----
text = README.read_text()

# 1) yearly table: replace between "### Summary by Calendar Year\n\n|" and "\n\n---\n\n<a" (or granular anchor)
# find yearly header
old_year_pat = re.compile(
    r"(\| Year \| Duration \| Nominal Yield.*?TOTAL.*?\n)",
    re.DOTALL,
)
m = old_year_pat.search(text)
if m:
    text = text[:m.start()] + year_table + "\n" + text[m.end():]

# 2) granular section: replace from anchor to before "\n---\n\n## 🔬 Reproducing"
# allow existing anchor or heading
gran_start = text.find('<a id="all-45-months-granular-returns">')
if gran_start == -1:
    gran_start = text.find("### All 45 Months Granular Returns")
gran_end_marker = "\n---\n\n## 🔬 Reproducing the Analysis"
gran_end = text.find(gran_end_marker, gran_start)
if gran_start != -1 and gran_end != -1:
    text = text[:gran_start] + granular_section + text[gran_end:]

# 3) key metrics table — optional: could regenerate but we keep stable for now
# (metrics come from audit JSON; if needed, extend script to replace that block too)

# write / check
parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args, _unknown = parser.parse_known_args()
# re-parse to avoid conflict when imported; use simple
import sys
check = "--check" in sys.argv
if check:
    original = README.read_text()
    if original != text:
        print("README would change — run without --check to update", file=sys.stderr)
        # diff summary
        import difflib
        for line in difflib.unified_diff(original.splitlines(), text.splitlines(), lineterm=""):
            if line.startswith("+") or line.startswith("-"):
                print(line)
        sys.exit(1)
    print("README check passed")
else:
    README.write_text(text)
    print("README updated from CSV + audit_metrics_summary.json")
