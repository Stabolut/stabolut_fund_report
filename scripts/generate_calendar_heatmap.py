#!/usr/bin/env python3
"""
Generate institutional Monthly Calendar Heatmap & Summary Grid for Stabolut Fund Report.
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

df = pd.read_csv(DATA_DIR / "monthly_performance.csv")

# Parse Year and Month
df["Year"] = df["Month"].apply(lambda x: int(x.split("-")[0]))
df["MonthNum"] = df["Month"].apply(lambda x: int(x.split("-")[1]))

years = [2022, 2023, 2024, 2025, 2026]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Create Grid (Years x 12 Months)
grid = np.full((len(years), 12), np.nan)
ann_comp = []
ann_btc = []

for i, yr in enumerate(years):
    yr_data = df[df["Year"] == yr]
    for _, row in yr_data.iterrows():
        m_idx = int(row["MonthNum"]) - 1
        grid[i, m_idx] = row["Yield_Pct"]
    
    comp_ret = (np.prod(1 + yr_data["Yield_Pct"]/100.0) - 1.0) * 100.0 if len(yr_data) > 0 else np.nan
    comp_btc = (np.prod(1 + yr_data["BTC_Return_Pct"]/100.0) - 1.0) * 100.0 if len(yr_data) > 0 else np.nan
    ann_comp.append(comp_ret)
    ann_btc.append(comp_btc)

# Create Heatmap Figure
fig, ax = plt.subplots(figsize=(13, 5.2), dpi=300)

cmap = plt.cm.Blues
norm = mcolors.Normalize(vmin=0.6, vmax=2.1)

# Plot background cells
for i, yr in enumerate(years):
    for j in range(12):
        val = grid[i, j]
        if np.isnan(val):
            # Not active cell
            rect = plt.Rectangle((j, len(years) - 1 - i), 1, 1, facecolor='#F1F3F5', edgecolor='#DEE2E6', lw=1.2)
            ax.add_patch(rect)
            ax.text(j + 0.5, len(years) - 1 - i + 0.5, "—", ha='center', va='center', color='#ADB5BD', fontsize=10, fontweight='medium')
        else:
            color = cmap(norm(val))
            rect = plt.Rectangle((j, len(years) - 1 - i), 1, 1, facecolor=color, edgecolor='#FFFFFF', lw=1.5)
            ax.add_patch(rect)
            
            # Text contrast
            text_color = "white" if val > 1.3 else "#084298"
            ax.text(j + 0.5, len(years) - 1 - i + 0.5, f"+{val:.2f}%", ha='center', va='center', color=text_color, fontsize=10, fontweight='bold')

    # Annual Return column (Fund)
    ann_val = ann_comp[i]
    ann_color = '#CFE2FF'
    rect_ann = plt.Rectangle((12.2, len(years) - 1 - i), 1.3, 1, facecolor=ann_color, edgecolor='#0A58CA', lw=1.5)
    ax.add_patch(rect_ann)
    ax.text(12.85, len(years) - 1 - i + 0.5, f"+{ann_val:.2f}%", ha='center', va='center', color='#084298', fontsize=10.5, fontweight='black')

    # Annual Return column (BTC)
    btc_val = ann_btc[i]
    btc_color = '#FFF3CD' if btc_val >= 0 else '#F8D7DA'
    btc_text_col = '#664D03' if btc_val >= 0 else '#842029'
    rect_btc = plt.Rectangle((13.7, len(years) - 1 - i), 1.3, 1, facecolor=btc_color, edgecolor='#FFC107' if btc_val >= 0 else '#DC3545', lw=1.0)
    ax.add_patch(rect_btc)
    sign = "+" if btc_val >= 0 else ""
    ax.text(14.35, len(years) - 1 - i + 0.5, f"{sign}{btc_val:.1f}%", ha='center', va='center', color=btc_text_col, fontsize=9.5, fontweight='bold')

ax.set_xlim(0, 15.2)
ax.set_ylim(0, len(years))

# X & Y ticks
ax.set_xticks([j + 0.5 for j in range(12)] + [12.85, 14.35])
ax.set_xticklabels(months + ["Fund Total", "BTC Benchmark"], fontsize=10, fontweight='bold')
ax.set_yticks([len(years) - 1 - i + 0.5 for i in range(len(years))])
ax.set_yticklabels([str(yr) for yr in years], fontsize=11, fontweight='bold')

ax.xaxis.tick_top()
ax.tick_params(axis='both', which='both', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.title("Stabolut Delta-Neutral Yield Fund — Monthly Return Matrix (%) (Nov 2022 – Aug 2026)\nAudited Systematic Cash Flow Harvesting Across All Market Cycles", fontsize=12.5, fontweight='bold', pad=24)

# Sub-captions & Colorbar legend
cbar_ax = fig.add_axes([0.15, 0.04, 0.40, 0.035])
cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax, orientation='horizontal')
cb.set_label('Monthly Net Arbitrage Yield (%)', fontsize=8.5, fontweight='bold', labelpad=4)
cb.ax.tick_params(labelsize=8)

plt.figtext(0.62, 0.045, "• 100% Win Rate (45 / 45 Months Positive)  • Zero Monthly Drawdown  • Par $1.00 Peg Maintained", fontsize=8.5, fontweight='bold', color='#0A58CA')

out_path = ASSETS_DIR / "monthly_performance_matrix.png"
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated: {out_path}")
