# NVDA–SPX Risk & Dependence Analysis (Step-by-step Build)

This repo starts intentionally minimal. We will implement modules together in small, testable steps.

## Planned modules
- `src/nvda_spx/data.py`      : download prices + compute returns
- `src/nvda_spx/ex_nvda.py`   : construct ex-NVDA series
- `src/nvda_spx/plotting.py`  : plotting helpers

## Suggested workflow
1. Implement one small function
2. Add a quick test in `tests/`
3. Commit to git with a clear message
