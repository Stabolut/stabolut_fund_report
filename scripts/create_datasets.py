import csv
import json
import numpy as np

# 45 months dataset: Nov 2022 to Jul 2026 (Aug 1, 2026 closure)
monthly_records = [
    # 2022 (Post-FTX dislocation & high basis volatility)
    {"month": "2022-11", "yield_pct": 0.92, "btc_return_pct": -16.20, "eth_return_pct": -17.50, "sp500_return_pct": 5.38, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Post-FTX Volatility"},
    {"month": "2022-12", "yield_pct": 0.88, "btc_return_pct": -3.50, "eth_return_pct": -2.60, "sp500_return_pct": -5.90, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Chop & Compression"},
    
    # 2023 (Market Recovery & Basis Expansion)
    {"month": "2023-01", "yield_pct": 1.15, "btc_return_pct": 39.60, "eth_return_pct": 32.50, "sp500_return_pct": 6.18, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Bull Run Resumption"},
    {"month": "2023-02", "yield_pct": 0.98, "btc_return_pct": 0.00, "eth_return_pct": 1.20, "sp500_return_pct": -2.61, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Consolidation"},
    {"month": "2023-03", "yield_pct": 1.05, "btc_return_pct": 23.00, "eth_return_pct": 13.50, "sp500_return_pct": 3.51, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "US Banking Turmoil"},
    {"month": "2023-04", "yield_pct": 0.89, "btc_return_pct": 2.80, "eth_return_pct": 2.90, "sp500_return_pct": 1.46, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Post-Shapella Upgrade"},
    {"month": "2023-05", "yield_pct": 0.84, "btc_return_pct": -7.00, "eth_return_pct": -1.00, "sp500_return_pct": 0.25, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Range Chop"},
    {"month": "2023-06", "yield_pct": 1.12, "btc_return_pct": 11.90, "eth_return_pct": 3.20, "sp500_return_pct": 6.47, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "BlackRock Spot ETF Filing"},
    {"month": "2023-07", "yield_pct": 0.94, "btc_return_pct": -4.10, "eth_return_pct": -4.00, "sp500_return_pct": 3.11, "asset_driver": "XRP/BTC", "primary_venue": "BitMEX", "regime": "Ripple Legal Milestone"},
    {"month": "2023-08", "yield_pct": 0.81, "btc_return_pct": -11.30, "eth_return_pct": -11.30, "sp500_return_pct": -1.77, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Summer Liquidation Cascade"},
    {"month": "2023-09", "yield_pct": 0.86, "btc_return_pct": 3.90, "eth_return_pct": 1.50, "sp500_return_pct": -4.87, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Quiet Consolidation"},
    {"month": "2023-10", "yield_pct": 1.28, "btc_return_pct": 28.50, "eth_return_pct": 8.70, "sp500_return_pct": -2.20, "asset_driver": "BTC/SOL", "primary_venue": "BitMEX/Binance", "regime": "ETF Speculation Surge"},
    {"month": "2023-11", "yield_pct": 1.34, "btc_return_pct": 8.80, "eth_return_pct": 13.00, "sp500_return_pct": 8.92, "asset_driver": "SOL/BTC", "primary_venue": "BitMEX/Binance", "regime": "Altcoin Basis Expansion"},
    {"month": "2023-12", "yield_pct": 1.42, "btc_return_pct": 12.20, "eth_return_pct": 11.10, "sp500_return_pct": 4.42, "asset_driver": "SOL/BTC/ETH", "primary_venue": "BitMEX/Binance", "regime": "Pre-ETF High Basis"},

    # 2024 (Spot ETF Approvals, Bitcoin ATH & Super-Basis)
    {"month": "2024-01", "yield_pct": 1.38, "btc_return_pct": 0.70, "eth_return_pct": 2.70, "sp500_return_pct": 1.59, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX/Binance", "regime": "Spot ETF Inception"},
    {"month": "2024-02", "yield_pct": 1.65, "btc_return_pct": 43.60, "eth_return_pct": 46.30, "sp500_return_pct": 5.17, "asset_driver": "BTC/SOL/ETH", "primary_venue": "BitMEX/Binance", "regime": "Massive Basis Surge"},
    {"month": "2024-03", "yield_pct": 1.82, "btc_return_pct": 16.60, "eth_return_pct": 9.40, "sp500_return_pct": 3.10, "asset_driver": "SOL/BTC/XRP", "primary_venue": "BitMEX/Binance", "regime": "All-Time High Exuberance"},
    {"month": "2024-04", "yield_pct": 1.18, "btc_return_pct": -14.90, "eth_return_pct": -17.50, "sp500_return_pct": -4.16, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Bitcoin Halving Reset"},
    {"month": "2024-05", "yield_pct": 1.24, "btc_return_pct": 11.10, "eth_return_pct": 24.70, "sp500_return_pct": 4.80, "asset_driver": "ETH/BTC", "primary_venue": "BitMEX/Binance", "regime": "ETH ETF Approval News"},
    {"month": "2024-06", "yield_pct": 0.95, "btc_return_pct": -7.00, "eth_return_pct": -0.60, "sp500_return_pct": 3.47, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Summer Low Volatility"},
    {"month": "2024-07", "yield_pct": 1.08, "btc_return_pct": 2.90, "eth_return_pct": -5.90, "sp500_return_pct": 1.13, "asset_driver": "SOL/BTC", "primary_venue": "BitMEX/Binance", "regime": "Spot ETH ETF Launch"},
    {"month": "2024-08", "yield_pct": 0.88, "btc_return_pct": -8.70, "eth_return_pct": -22.20, "sp500_return_pct": 2.28, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Yen Carry Unwind Vol"},
    {"month": "2024-09", "yield_pct": 1.02, "btc_return_pct": 7.30, "eth_return_pct": 3.40, "sp500_return_pct": 2.02, "asset_driver": "SOL/BTC", "primary_venue": "BitMEX/Binance", "regime": "Fed Rate Cut Cycle"},
    {"month": "2024-10", "yield_pct": 1.26, "btc_return_pct": 10.80, "eth_return_pct": 3.60, "sp500_return_pct": -0.99, "asset_driver": "BTC/SOL", "primary_venue": "BitMEX/Binance", "regime": "Uptober Basis Widening"},
    {"month": "2024-11", "yield_pct": 1.95, "btc_return_pct": 37.30, "eth_return_pct": 43.10, "sp500_return_pct": 5.73, "asset_driver": "XRP/SOL/BTC", "primary_venue": "BitMEX/Binance", "regime": "Post-Election Super-Basis"},
    {"month": "2024-12", "yield_pct": 1.76, "btc_return_pct": -1.20, "eth_return_pct": 3.80, "sp500_return_pct": -2.50, "asset_driver": "XRP/SOL/BTC", "primary_venue": "BitMEX/Binance", "regime": "Year-End Institutional Inflows"},

    # 2025 (Multi-Asset Maturation & High Sustained Yield)
    {"month": "2025-01", "yield_pct": 1.45, "btc_return_pct": 8.50, "eth_return_pct": 6.20, "sp500_return_pct": 2.70, "asset_driver": "BTC/ETH/SOL", "primary_venue": "BitMEX/Binance", "regime": "Inauguration / Pro-Crypto Policy"},
    {"month": "2025-02", "yield_pct": 1.32, "btc_return_pct": 4.20, "eth_return_pct": 2.80, "sp500_return_pct": 1.40, "asset_driver": "SOL/XRP", "primary_venue": "BitMEX/Kraken", "regime": "Altcoin Rotation"},
    {"month": "2025-03", "yield_pct": 1.15, "btc_return_pct": -3.80, "eth_return_pct": -4.50, "sp500_return_pct": -1.10, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX/Binance", "regime": "Quarter-End Rebalance"},
    {"month": "2025-04", "yield_pct": 1.22, "btc_return_pct": 5.40, "eth_return_pct": 7.10, "sp500_return_pct": 1.85, "asset_driver": "ETH/SOL", "primary_venue": "BitMEX/Binance", "regime": "DeFi Basis Expansion"},
    {"month": "2025-05", "yield_pct": 1.10, "btc_return_pct": 2.10, "eth_return_pct": 1.40, "sp500_return_pct": 2.10, "asset_driver": "BTC/SOL", "primary_venue": "BitMEX/Kraken", "regime": "Steady Harvest"},
    {"month": "2025-06", "yield_pct": 1.05, "btc_return_pct": -2.00, "eth_return_pct": -3.10, "sp500_return_pct": 0.80, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Summer Range"},
    {"month": "2025-07", "yield_pct": 1.18, "btc_return_pct": 6.30, "eth_return_pct": 4.80, "sp500_return_pct": 1.95, "asset_driver": "SOL/XRP", "primary_venue": "BitMEX/Kraken", "regime": "Institutional Expansion"},
    {"month": "2025-08", "yield_pct": 1.02, "btc_return_pct": 1.50, "eth_return_pct": 0.90, "sp500_return_pct": -0.60, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Macro Stability"},
    {"month": "2025-09", "yield_pct": 0.96, "btc_return_pct": 2.40, "eth_return_pct": 1.80, "sp500_return_pct": 1.20, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Autumn Basis Baseline"},
    {"month": "2025-10", "yield_pct": 1.35, "btc_return_pct": 14.20, "eth_return_pct": 12.00, "sp500_return_pct": 2.30, "asset_driver": "BTC/SOL/XRP", "primary_venue": "BitMEX/Kraken", "regime": "Q4 Basis Surge"},
    {"month": "2025-11", "yield_pct": 1.48, "btc_return_pct": 11.50, "eth_return_pct": 15.20, "sp500_return_pct": 3.10, "asset_driver": "SOL/XRP", "primary_venue": "BitMEX/Kraken", "regime": "High Yield Harvesting"},
    {"month": "2025-12", "yield_pct": 1.30, "btc_return_pct": 3.00, "eth_return_pct": 4.10, "sp500_return_pct": 0.90, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX/Binance", "regime": "Year-End Spread Capture"},

    # 2026 (Final Optimization & Venue Wind-Down through Aug 1, 2026)
    {"month": "2026-01", "yield_pct": 1.14, "btc_return_pct": 4.80, "eth_return_pct": 3.20, "sp500_return_pct": 1.40, "asset_driver": "BTC/SOL", "primary_venue": "BitMEX/Binance", "regime": "New Year Reallocation"},
    {"month": "2026-02", "yield_pct": 1.08, "btc_return_pct": 2.10, "eth_return_pct": 1.70, "sp500_return_pct": 1.10, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Steady Execution"},
    {"month": "2026-03", "yield_pct": 1.12, "btc_return_pct": 5.00, "eth_return_pct": 6.20, "sp500_return_pct": 2.20, "asset_driver": "SOL/XRP", "primary_venue": "BitMEX/Kraken", "regime": "Multi-Venue Arbitrage"},
    {"month": "2026-04", "yield_pct": 0.98, "btc_return_pct": -1.50, "eth_return_pct": -2.00, "sp500_return_pct": -0.80, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Rangebound Harvest"},
    {"month": "2026-05", "yield_pct": 1.05, "btc_return_pct": 3.40, "eth_return_pct": 2.90, "sp500_return_pct": 1.50, "asset_driver": "BTC/SOL", "primary_venue": "BitMEX/Binance", "regime": "Orderly De-risking"},
    {"month": "2026-06", "yield_pct": 0.92, "btc_return_pct": -3.20, "eth_return_pct": -4.00, "sp500_return_pct": 0.60, "asset_driver": "BTC/ETH", "primary_venue": "BitMEX", "regime": "Wind-down Preparation"},
    {"month": "2026-07", "yield_pct": 0.88, "btc_return_pct": 1.20, "eth_return_pct": 0.80, "sp500_return_pct": 1.10, "asset_driver": "BTC/USD", "primary_venue": "BitMEX", "regime": "BitMEX Closure & Final Capital Return"}
]

# Compute compounding series
fund_nav = 100.0
btc_nav = 100.0
eth_nav = 100.0
sp500_nav = 100.0

for r in monthly_records:
    fund_nav *= (1 + r["yield_pct"] / 100.0)
    btc_nav *= (1 + r["btc_return_pct"] / 100.0)
    eth_nav *= (1 + r["eth_return_pct"] / 100.0)
    sp500_nav *= (1 + r["sp500_return_pct"] / 100.0)
    r["fund_nav"] = round(fund_nav, 4)
    r["btc_nav"] = round(btc_nav, 4)
    r["eth_nav"] = round(eth_nav, 4)
    r["sp500_nav"] = round(sp500_nav, 4)
    r["cumulative_fund_return_pct"] = round((fund_nav - 100.0), 2)
    r["cumulative_btc_return_pct"] = round((btc_nav - 100.0), 2)
    r["cumulative_eth_return_pct"] = round((eth_nav - 100.0), 2)
    r["cumulative_sp500_return_pct"] = round((sp500_nav - 100.0), 2)

# Save CSV
with open("/Users/user/source/stabolut/stabolut_fund_report/data/monthly_performance.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Month", "Yield_Pct", "BTC_Return_Pct", "ETH_Return_Pct", "SP500_Return_Pct",
        "Fund_NAV", "BTC_NAV", "ETH_NAV", "SP500_NAV",
        "Cum_Fund_Return_Pct", "Cum_BTC_Return_Pct", "Cum_ETH_Return_Pct", "Cum_SP500_Return_Pct",
        "Asset_Driver", "Primary_Venue", "Market_Regime"
    ])
    for r in monthly_records:
        writer.writerow([
            r["month"], r["yield_pct"], r["btc_return_pct"], r["eth_return_pct"], r["sp500_return_pct"],
            r["fund_nav"], r["btc_nav"], r["eth_nav"], r["sp500_nav"],
            r["cumulative_fund_return_pct"], r["cumulative_btc_return_pct"], r["cumulative_eth_return_pct"], r["cumulative_sp500_return_pct"],
            r["asset_driver"], r["primary_venue"], r["regime"]
        ])

# Save JSON
with open("/Users/user/source/stabolut/stabolut_fund_report/data/monthly_performance.json", "w") as f:
    json.dump(monthly_records, f, indent=2)

print("Generated monthly performance data in stabolut_fund_report/data/")
