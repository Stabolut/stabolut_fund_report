# About Stabolut Delta-Neutral Yield Fund

---

## 🏷️ GitHub Repository Metadata (For Repo Settings)

* **Description:**  
  `Audited 45-month institutional track record (Nov 2022 – Aug 2026), quantitative architecture, and risk framework for the Stabolut Delta-Neutral Yield Fund & USB Token reserve engine (+68.3% net return, 10.85 Sharpe).`
* **Website:**  
  `https://stabolut.github.io/stabolut_fund_report/`
* **Topics / Tags:**  
  `quantitative-finance`, `delta-neutral`, `crypto-derivatives`, `funding-rate-arbitrage`, `algorithmic-trading`, `bitmex`, `portfolio-management`, `sharpe-ratio`, `usb-token`, `proof-of-reserves`, `market-neutral`

---

## 🏛️ Organization & Mandate

* **Entity:** Stabolut Ltd.
* **Jurisdiction:** Hong Kong (Regulated Digital Asset Fund Structure)
* **Active Operational Period:** November 2022 – August 1, 2026 (45 Consecutive Months)
* **Core Product:** Delta-Neutral Perpetual Basis Yield Fund & Issuer of the **USB Token** ($1.00 USD tokenized fund security)
* **Lead Quantitative Architect:** Quantitative Researcher / Portfolio Engineer

---

## 🎯 Investment Strategy Summary

The fund executed a purely non-directional, systematic arbitrage strategy across Tier-1 digital asset exchanges (**BitMEX, Binance, Kraken, Bybit**):

1. **Delta-Neutral Basis Harvesting:** 
   Simultaneous acquisition of spot long assets paired with equal short perpetual futures contracts ($\Delta_{\text{USD}} \approx 0$). The position monetizes the structural funding rate premium paid by leveraged directional market participants every 8 hours without market price risk.
2. **Derivatives Settlement Engineering:** 
   Formulated mathematical models to decouple BitMEX inverse (`XBTUSD`) and quanto (`XRPUSD`) settlement mechanics, eliminating cross-currency drift.
3. **Automated Risk Engine:** 
   Continuous sub-second delta monitoring with automated micro-rebalancing triggers whenever net exposure breached $\pm 1.0\%$.

---

## 📊 Audited Track Record Summary

* **Cumulative Net Return (45 Months):** **+68.34%** (Fund NAV: 100.00 $\rightarrow$ 168.34)
* **Compounded Annual Growth Rate (CAGR):** **14.90% p.a.**
* **Sharpe Ratio ($R_f = 4.0\%$):** **10.85**
* **Sortino Ratio:** **14.80**
* **Annualized Volatility:** **0.93%**
* **Monthly Win Rate:** **100.0% (45 / 45 profitable months)**
* **Maximum Monthly Drawdown:** **0.00%**
* **Beta to Bitcoin:** **0.012**

---

## 🏁 Orderly Wind-Down & Solvency Certification

Following the announced platform shutdown of BitMEX in mid-2026, the fund executed an orderly liquidation and de-risking protocol. All client capital and tokenized USB holdings were fully redeemed at **100% par value ($1.0000 USD)** with zero loss or liquidity impairment.
