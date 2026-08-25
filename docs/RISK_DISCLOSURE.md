# Institutional Risk Disclosures & Mitigations

While the Stabolut Delta-Neutral strategy eliminated directional price risk, quantitative execution in cryptocurrency derivatives requires comprehensive risk frameworks to manage non-directional exposure vectors.

---

## 1. Risk Vector Breakdown & Engineering Safeguards

### 1.1 Basis Inversion & Negative Funding
* **Risk:** During prolonged market drawdowns or extreme panic selling, perpetual funding rates can turn negative ($F < 0$), requiring short holders to pay longs.
* **Mitigation:** The quant system deployed a 30-day moving average funding filter. When an asset's funding yields declined below the threshold ($< 3.0\%$ annualized), capital was systematically rotated into higher-basis assets (e.g. moving from BTC into SOL or XRP).

### 1.2 Execution Slippage & Rebalance Latency
* **Risk:** Rapid price jumps could cause transient delta deviation before rebalancing triggers execute.
* **Mitigation:** Tolerance thresholds were constrained to $|\Delta_{\text{USD}}| < 1.0\%$. Orders were split into TWAP/VWAP tranches via CCXT with limit order resting to capture liquidity maker rebates.

### 1.3 Exchange Counterparty & Liquidity Risk
* **Risk:** Venue insolvency or sudden trading halts on primary exchanges.
* **Mitigation:** Capital was distributed across multiple venues (BitMEX, Binance, Kraken, Bybit). When BitMEX announced its wind-down, risk systems executed orderly de-risking and full capital return without loss.

### 1.4 Quanto Cross-Currency Settlement Drift
* **Risk:** BitMEX quanto contracts (e.g., XRPUSD) settle margin in Bitcoin (XBT), exposing the position to BTC/USD fluctuations.
* **Mitigation:** Real-time calculation of $\gamma_{\text{BTC}}$ and automated micro-hedging via XBTUSD inverse contracts.
