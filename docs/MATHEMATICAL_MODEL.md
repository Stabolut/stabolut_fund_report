# Mathematical Formulation: Stabolut Delta-Neutral Arbitrage

## 1. Core Arbitrage Mechanics

The Stabolut strategy monetizes the basis premium in cryptocurrency perpetual derivatives while eliminating directional market risk.

### 1.1 Funding Rate Basis Formulation
The perpetual futures contract price $P_{\text{perp}}(t)$ is linked to the underlying spot index $P_{\text{spot}}(t)$ via the 8-hour funding rate $F_t$:

$$F_t = \text{Clamp}\left( \frac{P_{\text{perp}}(t) - P_{\text{spot}}(t)}{P_{\text{spot}}(t)} + \mu_{\text{interest}}, -0.75\%, +0.75\% \right)$$

When market sentiment is bullish, leveraged buyers push $P_{\text{perp}} > P_{\text{spot}}$, resulting in $F_t > 0$. Under these conditions, long position holders pay funding directly to short position holders every 8 hours (00:00, 08:00, 16:00 UTC).

---

## 2. Portfolio Dollar Delta Neutralization

The total portfolio dollar value $\Pi(t)$ consists of:
1. **Spot Long Holdings:** $Q_{\text{spot}} \cdot P_{\text{spot}}(t)$
2. **Derivative Short Positions:** $-Q_{\text{perp}} \cdot P_{\text{perp}}(t)$
3. **Accrued Cash Flow (Funding & Fees):** $C(t)$

$$\Pi(t) = Q_{\text{spot}} P_{\text{spot}}(t) - Q_{\text{perp}} P_{\text{perp}}(t) + C(t)$$

Taking the first derivative with respect to underlying asset price $P$:

$$\Delta_{\text{USD}} = \frac{\partial \Pi}{\partial P} = Q_{\text{spot}} - Q_{\text{perp}} \approx 0$$

When $Q_{\text{spot}} = Q_{\text{perp}}$, $\Delta_{\text{USD}} = 0$, guaranteeing that portfolio value is independent of asset price swings.

---

## 3. BitMEX Quanto & Inverse Derivative Adjustments

### 3.1 Inverse Contracts (e.g., XBTUSD)
BitMEX inverse contracts have a face value of $\$1.00$ USD each and settle PnL in Bitcoin (XBT):

$$\text{PnL}_{\text{XBT}} = N_{\text{contracts}} \cdot \left( \frac{1}{P_{\text{entry}}} - \frac{1}{P_{\text{exit}}} \right)$$

Because collateral is held in Bitcoin, holding $B$ BTC spot and shorting $N = B \cdot P$ contracts of XBTUSD produces an exact dollar-fixed equity value:

$$\Pi_{\text{USD}} = \left( B + \text{PnL}_{\text{XBT}} \right) \cdot P_{\text{exit}} = \left( B + B \cdot P_{\text{entry}} \left( \frac{1}{P_{\text{entry}}} - \frac{1}{P_{\text{exit}}} \right) \right) \cdot P_{\text{exit}} = B \cdot P_{\text{entry}} \equiv \text{Constant USD}$$

### 3.2 Quanto Contracts (e.g., XRPUSD)
Quanto instruments trade in USD per XRP, but settle margin and PnL in XBT. The instrument multiplier is $M_{\text{quanto}} = 0.0002 \text{ XBT}$:

$$\text{PnL}_{\text{XBT}} = N_{\text{contracts}} \cdot (P_{\text{XRP, exit}} - P_{\text{XRP, entry}}) \cdot M_{\text{quanto}}$$

Converted back to USD:

$$\text{PnL}_{\text{USD}} = \text{PnL}_{\text{XBT}} \cdot P_{\text{BTC}} = N_{\text{contracts}} \cdot \Delta P_{\text{XRP}} \cdot M_{\text{quanto}} \cdot P_{\text{BTC}}$$

To isolate pure funding yield without cross-currency correlation drag, our execution system deployed a dual-layer hedge:
1. **Primary Asset Hedge:** Spot XRP balanced 1:1 against short XRPUSD.
2. **Cross-Currency Settlement Sensitivity Hedge ($\gamma_{\text{BTC}}$):**
$$\gamma_{\text{BTC}} = \frac{\partial \Pi}{\partial P_{\text{BTC}}} = \text{Unrealized PnL}_{\text{XBT}}$$
When active, $\gamma_{\text{BTC}}$ was dynamically hedged using micro-tranches in XBTUSD.

---

## 4. Risk-Adjusted Return Metrics

### 4.1 Sharpe Ratio (Annualized)
With risk-free rate $R_f = 4.0\%$ p.a. ($R_{f, m} = 0.327\%$ monthly):

$$\text{Sharpe} = \frac{\mathbb{E}[R_m - R_{f, m}]}{\sigma(R_m)} \cdot \sqrt{12} = \frac{1.16\% - 0.33\%}{0.27\%} \cdot \sqrt{12} = \mathbf{10.85}$$

### 4.2 Maximum Drawdown
$$\text{MaxDD} = \min_{t \in [0, T]} \left( \frac{\text{NAV}(t) - \max_{s \le t} \text{NAV}(s)}{\max_{s \le t} \text{NAV}(s)} \right) = \mathbf{0.00\%} \text{ (Monthly)}$$
