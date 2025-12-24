# NVDA–SPX Risk & Dependence Analysis

This project investigates how much of the S&P 500’s recent risk and return dynamics can be attributed to NVIDIA (NVDA). Using an ex-NVDA decomposition of the index, the analysis examines historical co-movement, scenario-based shocks, and portfolio implications under different assumptions about NVDA’s future behavior.

## Planned modules
- `src/nvda_spx/data.py`      : download prices + compute returns
- `src/nvda_spx/ex_nvda.py`   : construct ex-NVDA series
- `src/nvda_spx/plotting.py`  : plotting helpers
