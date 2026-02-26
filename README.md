# NVDA–SPX Structural Sensitivity Analysis

## Overview

This project evaluates how sensitive S&P 500 (SPX) drawdown behavior is to structural exposure assumptions for a dominant index constituent, using NVIDIA (NVDA) as an illustrative case study.

Rather than attempting to estimate causal influence, the analysis adopts a simplified linear decomposition framework to examine how simulated stress outcomes vary with assumed NVDA exposure weights.

The project is designed as a methodological sensitivity study rather than an investment thesis.

## Research Question

Under a linear return decomposition:

$$ r_{SPX} = wr_{NVDA} + (1-w)r_{exNVDA} $$

how do simulated SPX drawdowns respond to:

* different NVDA shock magnitudes?
* different structural exposure assumptions $w$?

## Key Findings

* **Rolling beta analysis**: NVDA has frequently exhibited elevated rolling beta relative to SPX, particularly during early 2020 and throughout 2025, suggesting sustained periods of strong statistical association.
* **Shock simulations**: Simulated one-day NVDA shocks produce index drawdowns that scale mechanically with both shock magnitude and assumed NVDA weight.
* **Sensitivity analysis**: Stress conclusions are materially dependent on structural exposure assumptions. Larger assumed weights significantly amplify simulated drawdowns.
* **Persistence asymmetry**: In the stylized framework, depth of stress is more sensitive to exposure assumptions than recovery duration.

## Methodology

1. Daily adjusted returns obtained via `yfinance`
2. Linear decomposition of SPX into NVDA and ex-NVDA components
3. Rolling beta estimation (60/120/252-day windows)
4. Stylized one-day NVDA shock simulations
5. Drawdown and recovery metrics computed relative to pre-shock level
6. Sensitivity grid evaluated across exposure weights and shock magnitudes

## Limitations

This framework is intentionally stylized and excludes:

* Time-varying index weights
* Nonlinear dynamics
* Volatility clustering
* Endogenous feedback or contagion effects
* Multi-day shock propagation

Results should be interpreted as structural stress sensitivity analysis under simplified assumptions rather than as forecasts.

## Repository Structure

```
src/nvda_spx/
    data.py
    ex_nvda.py
    scenarios.py
    metrics.py
    plotting.py

notebooks/
    00_report.ipynb        # Final structured report
    01_explore_ex_nvda.ipynb  # Exploratory analysis

reports/
    00_report.html         # Static HTML version of final report
    00_report.pdf          # Static PDF version of final report
```

## How to Run

1. Create a virtual environment
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Open `notebooks/00_report.ipynb`
4. Run all cells

For readers who prefer not to set up a local Python environment, the static report can be viewed directly:

- `reports/00_report.pdf`
- `reports/00_report.html`

The fully reproducible source notebook is available at:

- `notebooks/00_report.ipynb`

## Potential Extensions

* Time-varying exposure estimation
* Multi-day shock paths
* Volatility modeling
* Cross-constituent comparison

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
