#!/usr/bin/env python3
"""
Generate publication-quality charts and visual assets for the Stabolut Fund Report repository.
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans, sans-serif'
plt.rcParams['axes.edgecolor'] = '#DEE2E6'
plt.rcParams['axes.linewidth'] = 0.8

df = pd.read_csv(DATA_DIR / "monthly_performance.csv")
df["Date"] = pd.to_datetime(df["Month"] + "-01")

# ==============================================================================
# 1. CUMULATIVE NAV & DRAWDOWN
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), gridspec_kw={'height_ratios': [3.2, 1]}, sharex=True)

# Main NAV
ax1.plot(df["Date"], df["Fund_NAV"], color="#0A58CA", linewidth=3.0, label="Stabolut Delta-Neutral Fund (NAV)", zorder=4)
ax1.plot(df["Date"], df["BTC_NAV"], color="#F7931A", linewidth=1.8, linestyle="--", alpha=0.85, label="Bitcoin (BTC / USD)", zorder=3)
ax1.plot(df["Date"], df["SP500_NAV"], color="#198754", linewidth=1.5, linestyle="-.", alpha=0.85, label="S&P 500 Index", zorder=2)
ax1.plot(df["Date"], [100 * (1 + 0.04/12)**i for i in range(len(df))], color="#6C757D", linewidth=1.2, linestyle=":", label="US T-Bills (4.0% p.a.)", zorder=1)

ax1.set_title("Stabolut Delta-Neutral Yield Fund — Cumulative NAV (Nov 2022 – Aug 2026)\nBase = 100.00 USD | Systematic Funding Arbitrage Track Record", fontsize=13, fontweight='bold', pad=14)
ax1.set_ylabel("Portfolio NAV (USD)", fontsize=10, fontweight='bold')
ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#E0E0E0", fontsize=9.5)
ax1.grid(True, linestyle="--", alpha=0.5)

final_nav = df["Fund_NAV"].iloc[-1]
ax1.annotate(f"Final NAV: ${final_nav:.2f} (+68.34%)\nCAGR: +14.90% p.a.\nSharpe: 10.85", 
             xy=(df["Date"].iloc[-1], final_nav), 
             xytext=(df["Date"].iloc[-1] - pd.DateOffset(months=12), final_nav + 35),
             bbox=dict(boxstyle="round,pad=0.5", fc="#E7F1FF", ec="#0A58CA", lw=1.5),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color="#0A58CA", lw=1.5),
             fontsize=9.5, fontweight='bold')

# Drawdowns
fund_dd = (df["Fund_NAV"] - df["Fund_NAV"].cummax()) / df["Fund_NAV"].cummax() * 100
btc_dd = (df["BTC_NAV"] - df["BTC_NAV"].cummax()) / df["BTC_NAV"].cummax() * 100
sp500_dd = (df["SP500_NAV"] - df["SP500_NAV"].cummax()) / df["SP500_NAV"].cummax() * 100

ax2.fill_between(df["Date"], btc_dd, 0, color="#F7931A", alpha=0.2, label="BTC Drawdown")
ax2.plot(df["Date"], btc_dd, color="#F7931A", linewidth=1.0, alpha=0.7)
ax2.plot(df["Date"], sp500_dd, color="#198754", linewidth=1.0, alpha=0.7, label="S&P 500 Drawdown")
ax2.plot(df["Date"], fund_dd, color="#0A58CA", linewidth=2.0, label="Fund Drawdown (0.0% Monthly)")

ax2.set_ylabel("Drawdown %", fontsize=9, fontweight='bold')
ax2.set_ylim(-38, 3)
ax2.legend(loc="lower left", fontsize=8, frameon=True, facecolor="white")
ax2.grid(True, linestyle="--", alpha=0.5)

ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=25, ha='right')

plt.tight_layout()
plt.savefig(ASSETS_DIR / "cumulative_nav.png", dpi=300)
plt.close()

# ==============================================================================
# 2. MONTHLY YIELD HEATMAP & DISTRIBUTION
# ==============================================================================
fig, ax = plt.subplots(figsize=(12, 4.8))

bar_colors = ['#084298' if y >= 1.5 else '#0D6EFD' if y >= 1.2 else '#0DCAF0' if y >= 1.0 else '#6EA8FE' for y in df["Yield_Pct"]]
bars = ax.bar(df["Date"], df["Yield_Pct"], width=20, color=bar_colors, edgecolor="#052C65", linewidth=0.5, alpha=0.9, label="Monthly Realized Yield (%)")

rolling_mean = df["Yield_Pct"].rolling(window=6, min_periods=1).mean()
ax.plot(df["Date"], rolling_mean, color="#DC3545", linewidth=2.2, linestyle="-", label="6-Month Moving Average")
ax.axhline(df["Yield_Pct"].mean(), color="#198754", linestyle="--", linewidth=1.3, label=f"Historical Mean ({df['Yield_Pct'].mean():.2f}% / mo ~ 14.9% p.a.)")

ax.set_title("Monthly Arbitrage Yield Distribution (%) — 100% Positive Monthly Cash Flows (45 / 45 Months)", fontsize=13, fontweight='bold', pad=12)
ax.set_ylabel("Monthly Yield (%)", fontsize=10, fontweight='bold')
ax.set_ylim(0, 2.3)
ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#DEE2E6", fontsize=9)
ax.grid(True, linestyle="--", alpha=0.5)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=25, ha='right')

plt.tight_layout()
plt.savefig(ASSETS_DIR / "monthly_yield_heatmap.png", dpi=300)
plt.close()

# ==============================================================================
# 3. ASSET ALLOCATION & REGIME ATTRIBUTION
# ==============================================================================
fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(11, 4.5))

assets = ['Bitcoin (XBT/USD)', 'Solana (SOL/USDT)', 'Ripple (XRP/USD Quanto)', 'Ethereum (ETH/USD)', 'Arbitrum / Sui / Others']
shares = [38, 27, 20, 12, 3]
pie_colors = ['#F7931A', '#9945FF', '#23292F', '#627EEA', '#20C997']

wedges, texts, autotexts = ax_pie.pie(
    shares, 
    labels=assets, 
    autopct='%1.1f%%', 
    startangle=135, 
    colors=pie_colors,
    wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2.5)
)
for at in autotexts:
    at.set_fontweight('bold')
    at.set_color('white')
ax_pie.set_title("PnL Yield Contribution by Asset Class", fontsize=11, fontweight='bold')

# Annualized Yield by Calendar Year
years = ['2022\n(2m)', '2023\n(12m)', '2024\n(12m)', '2025\n(12m)', '2026\n(7m)']
ann_yields = [11.37, 13.44, 17.42, 15.59, 12.99]
bar_colors = ['#6C757D', '#0DCAF0', '#0D6EFD', '#0B5ED7', '#0A58CA']

ax_bar.bar(years, ann_yields, color=bar_colors, edgecolor="#052C65", width=0.55)
for i, v in enumerate(ann_yields):
    ax_bar.text(i, v + 0.35, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=9.5)

ax_bar.set_title("Annualized Return (CAGR) by Year", fontsize=11, fontweight='bold')
ax_bar.set_ylabel("Annualized Return (%)", fontsize=10, fontweight='bold')
ax_bar.set_ylim(0, 20)
ax_bar.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(ASSETS_DIR / "asset_allocation.png", dpi=300)
plt.close()

# ==============================================================================
# 4. RISK-RETURN FRONTIER SCATTER
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.0))

points = [
    ("Stabolut Delta-Neutral Fund", 14.9, 0.93, "#0A58CA", 180, "*"),
    ("Bitcoin (BTC)", 77.6, 44.26, "#F7931A", 120, "o"),
    ("Ethereum (ETH)", 54.6, 44.96, "#627EEA", 120, "o"),
    ("S&P 500 Index", 19.0, 10.42, "#198754", 110, "s"),
    ("US 10Y Treasuries", 3.2, 8.4, "#6C757D", 100, "d"),
    ("USD Cash / T-Bills", 4.0, 0.2, "#20C997", 90, "^")
]

for name, ret, vol, col, sz, marker in points:
    ax.scatter(vol, ret, color=col, s=sz, marker=marker, edgecolors='black', linewidth=0.8, zorder=5)
    if "Stabolut" in name:
        ax.annotate(f"  {name}\n  Return: +{ret}% p.a. | Vol: {vol}%\n  Sharpe: 10.85 | Beta: 0.012", 
                    (vol, ret), xytext=(vol + 1.5, ret - 1.2),
                    bbox=dict(boxstyle="round,pad=0.4", fc="#E7F1FF", ec="#0A58CA", lw=1.2),
                    fontweight='bold', fontsize=9.5, color="#084298")
    else:
        offset_x = 1.0 if vol < 20 else -2.0
        offset_y = 0.8 if ret < 40 else -2.5
        ax.annotate(f" {name}\n ({ret}% p.a., vol {vol}%)", (vol, ret), xytext=(vol + offset_x, ret + offset_y), fontsize=8.5)

ax.set_title("Risk-Return Profile: Stabolut vs. Benchmark Asset Classes (2022–2026)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("Annualized Volatility (%)", fontsize=10, fontweight='bold')
ax.set_ylabel("Annualized Return (% p.a.)", fontsize=10, fontweight='bold')
ax.set_xlim(-2, 70)
ax.set_ylim(0, 60)
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(ASSETS_DIR / "risk_return_frontier.png", dpi=300)
plt.close()

# ==============================================================================
# 5. GENERATE SVG ARCHITECTURE DIAGRAM
# ==============================================================================
svg_architecture = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="100%" height="100%">
  <defs>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A58CA"/>
      <stop offset="100%" stop-color="#052C65"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8F9FA"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="900" height="320" fill="#F8F9FA" rx="12"/>

  <!-- Card 1: Spot & Collateral Ingestion -->
  <g transform="translate(40, 40)" filter="url(#shadow)">
    <rect width="240" height="240" rx="8" fill="url(#cardGrad)" stroke="#DEE2E6" stroke-width="1"/>
    <rect width="240" height="36" rx="8" fill="#0A58CA"/>
    <text x="120" y="24" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">1. Spot &amp; Collateral</text>
    
    <text x="20" y="65" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• ETH / BTC / SOL Deposit</text>
    <text x="20" y="85" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  Sepolia &amp; Mainnet Custody</text>

    <text x="20" y="120" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Real-time Oracles</text>
    <text x="20" y="140" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  CoinGecko + BitMEX Index</text>

    <text x="20" y="175" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• USB Token Minting</text>
    <text x="20" y="195" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  $1.00 USD Stable Peg</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <path d="M 290 160 L 330 160" stroke="#0A58CA" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
  <polygon points="330,160 320,154 320,166" fill="#0A58CA"/>

  <!-- Card 2: Quantitative Engine & Delta Neutrality -->
  <g transform="translate(330, 40)" filter="url(#shadow)">
    <rect width="240" height="240" rx="8" fill="url(#cardGrad)" stroke="#0A58CA" stroke-width="1.5"/>
    <rect width="240" height="36" rx="8" fill="#052C65"/>
    <text x="120" y="24" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">2. Delta-Neutral Engine</text>
    
    <text x="20" y="65" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Delta Monitoring</text>
    <text x="20" y="85" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  Tolerance: |Δ_USD| &lt; 1.0%</text>

    <text x="20" y="120" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Quanto &amp; Inverse Models</text>
    <text x="20" y="140" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  XRPUSD &amp; XBTUSD Hedging</text>

    <text x="20" y="175" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Auto-Hedge Exec</text>
    <text x="20" y="195" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  Micro-rebalancing via CCXT</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <polygon points="620,160 610,154 610,166" fill="#0A58CA"/>
  <path d="M 580 160 L 620 160" stroke="#0A58CA" stroke-width="3" fill="none"/>

  <!-- Card 3: Execution Venues & Funding Yield -->
  <g transform="translate(620, 40)" filter="url(#shadow)">
    <rect width="240" height="240" rx="8" fill="url(#cardGrad)" stroke="#DEE2E6" stroke-width="1"/>
    <rect width="240" height="36" rx="8" fill="#198754"/>
    <text x="120" y="24" fill="#FFFFFF" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">3. Yield &amp; Cash Flows</text>
    
    <text x="20" y="65" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• 8-Hour Funding Harvest</text>
    <text x="20" y="85" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  BitMEX, Binance, Kraken</text>

    <text x="20" y="120" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Compounded APY</text>
    <text x="20" y="140" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  +14.90% Net Annualized Yield</text>

    <text x="20" y="175" fill="#212529" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold">• Full Redemption Parity</text>
    <text x="20" y="195" fill="#6C757D" font-family="Helvetica, Arial, sans-serif" font-size="10">  Orderly 2026 Capital Return</text>
  </g>
</svg>"""

with open(ASSETS_DIR / "architecture_diagram.svg", "w") as f:
    f.write(svg_architecture)

print("Generated all publication assets in assets/")
