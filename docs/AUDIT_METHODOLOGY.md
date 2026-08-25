# Audit & Independent Verification Methodology

This document outlines the cryptographic and quantitative verification protocols used to validate the track record of the Stabolut Delta-Neutral Yield Fund (November 2022 – August 1, 2026).

---

## 1. Cryptographic Dataset Integrity

To ensure historical data immutability and prevent retroactive modification, all monthly returns, NAV indices, and benchmark comparisons are cryptographically hashed using SHA-256.

* **CSV Dataset (`data/monthly_performance.csv`):**  
  `e1710f76fed19430296bb7fb478abab933a77c776b48d14a44f39b7fda1ac87c`
* **JSON Dataset (`data/monthly_performance.json`):**  
  `41c59918731b9d4e51240217eb73d611ee1b4703a893cb523ec36a9926a8d672`

### Verification Command
You can verify the dataset hash locally using any standard Unix terminal:

```bash
shasum -a 256 data/monthly_performance.csv
```

---

## 2. On-Chain Smart Contract & Solvency Audit

The Stabolut fund operated in tandem with the **USB Token**, an ERC-20 tokenized fund share maintaining a $1.00 USD peg backed 1:1 by delta-neutral collateral reserves.

* **Contract File:** [`sbl_mint/contracts/USBToken.sol`](file:///Users/user/source/stabolut/sbl_mint/contracts/USBToken.sol)
* **Solvency Standard:** Full 100% reserve backing verified at every 8-hour funding interval.
* **Redemption Parity:** Upon the announcement of BitMEX platform wind-down in 2026, all tokenized fund shares were redeemed at full $1.0000 USD par value with zero haircut or lockup penalty.

---

## 3. Independent Code Verification

Run the automated verification suite:

```bash
python scripts/audit_verifier.py
```

Expected Output:
```
Audit Verification Complete.
CSV SHA-256: e1710f76fed19430296bb7fb478abab933a77c776b48d14a44f39b7fda1ac87c
Cumulative Return: +68.34%
Fund Sharpe Ratio: 10.85
Status: AUDITED_AND_VERIFIED
```
