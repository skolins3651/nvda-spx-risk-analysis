from __future__ import annotations

import pandas as pd

def ex_nvda_return(
    spx_ret: pd.Series,
    nvda_ret: pd.Series,
    weight: float | pd.Series,
) -> pd.Series:
    """
    Compute the ex-NVDA return series: r_ex = (r_spx - w * r_nvda) / (1 - w).
    Weight can be a constant float or a time-varying pd.Series aligned to spx_ret.
    """
    spx_ret = spx_ret.copy() # avoid modifying input data
    nvda_ret = nvda_ret.copy() # avoid modifying input data

    if isinstance(weight, (float, int)):
        w = pd.Series(float(weight), index=spx_ret.index) # convert scalar weight to time series
    else:
        w = weight.reindex(spx_ret.index) # align weight series to spx_ret index

    # cover for various error cases on weights
    if w.isna().any():
        raise ValueError("Weight series contains NaNs after alignment; cannot compute ex-NVDA returns.")
    if (w >= 1).any():
        raise ValueError("NVDA weight must be strictly less than 1 to compute ex-NVDA returns.")
    if (w < 0).any():
        raise ValueError("NVDA weight must be non-negative to compute ex-NVDA returns.")

    ex_ret = (spx_ret - w * nvda_ret) / (1 - w)
    ex_ret.name = "SPX_exNVDA"
    
    return ex_ret