from __future__ import annotations

import pandas as pd

def shocked_spx_return(
    ex_ret: pd.Series,
    weight: float | pd.Series,
    shock_return: float,
    shock_date: str | pd.Timestamp,
) -> pd.Series:
    """
    Return a counterfactual implied SPX return series where on `shock_date`,
    NVDA's return is replaced by `shock_return`, while ex-NVDA returns are unchanged.

    Uses: r_spx = w * r_nvda + (1 - w) * r_ex
    """
    ex_ret = ex_ret.copy() # avoid modifying input data

    if isinstance(weight, (float, int)):
        w = pd.Series(float(weight), index=ex_ret.index) # convert scalar weight to time series
    else:
        w = weight.reindex(ex_ret.index) # align weight series to spx_ret index

    # cover for various error cases on weights
    if w.isna().any():
        raise ValueError("Weight series contains NaNs after alignment.")
    if (w < 0).any() or (w >= 1).any():
        raise ValueError("Weight must satisfy 0 <= w < 1.")

    # cover for shock_date not appearing in the index
    shock_date = pd.Timestamp(shock_date)
    if shock_date not in ex_ret.index:
        raise KeyError(f"shock_date {shock_date.date()} not found in ex_ret index.")

    # cover for impossible shock_return values
    if shock_return <= -1:
        raise ValueError("shock_return must be greater than -1 (cannot lose more than 100% in one day).")

    # cover for NaN on shock_date in ex_ret
    if pd.isna(ex_ret.loc[shock_date]):
        raise ValueError("ex_ret is NaN on shock_date; cannot compute shocked return.")

    # baseline: assume NVDA return = 0 on non-shock days
    spx_base = (1 - w) * ex_ret
    spx_base.name = "SPX_shocked"
    
    spx_shocked = spx_base.copy()
    spx_shocked.loc[shock_date] = w.loc[shock_date] * shock_return + (1 - w.loc[shock_date]) * ex_ret.loc[shock_date]

    return spx_shocked

def shocked_spx_returns(
    ex_ret: pd.Series,
    weight: float | pd.Series,
    shock_returns: list[float],
    shock_date: str | pd.Timestamp,
) -> pd.DataFrame:
    """
    Compute multiple shocked SPX return series for different NVDA shock magnitudes.
    """
    shocked_cols: dict[str, pd.Series] = {}

    for s in shock_returns:
        col_name = f"SPX_shock_{int(round(s * 100))}pct"
        shocked_cols[col_name] = shocked_spx_return(
            ex_ret=ex_ret,
            weight=weight,
            shock_return=s,
            shock_date=shock_date,
        )

    return pd.DataFrame(shocked_cols)
