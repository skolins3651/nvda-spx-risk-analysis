import pandas as pd

def drawdown_metrics(
    returns: pd.Series,
    shock_date: str | pd.Timestamp,
) -> dict[str, object]:
    """
    Compute post-shock drawdown metrics relative to the pre-shock level.
    Metrics include: maximum drawdown, date of drawdown, and time to recovery.
    """
    shock_date = pd.Timestamp(shock_date)

    if shock_date not in returns.index:
        raise KeyError(f"shock_date {shock_date.date()} not found in returns index.")

    if pd.isna(returns.loc[shock_date]):
        raise ValueError("Return is NaN on shock_date; cannot compute drawdown metrics.")
    
    # recompute the level path from the returns
    growth = (1 + returns).cumprod()

    shock_loc = growth.index.get_loc(shock_date)
    if shock_loc == 0:
        raise ValueError("shock_date is the first observation; no pre-shock level exists.")

    pre_level = growth.iloc[shock_loc - 1] # defines pre-shock at just before shock_date

    post = growth.iloc[shock_loc:]  # from shock day onward
    dd = post / pre_level - 1

    max_dd = dd.min()
    max_dd_date = dd.idxmin()

    recovered = post >= pre_level # recovery means exceeding pre-shock level
    if recovered.any():
        recovery_date = post.index[recovered.argmax()]
        days_to_recovery = int((post.index.get_loc(recovery_date)))
    else:
        recovery_date = None
        days_to_recovery = None

    return {
        "shock_date": shock_date,
        "pre_shock_level": float(pre_level),
        "max_drawdown": float(max_dd),
        "max_drawdown_date": max_dd_date,
        "recovery_date": recovery_date,
        "days_to_recovery": days_to_recovery,
    }

def summarize_shock_scenarios(
    shocked_returns: pd.DataFrame,
    shock_date: str | pd.Timestamp,
) -> pd.DataFrame:
    """
    Apply drawdown_metrics to each column of `shocked_returns` and return a summary table.
    """
    shock_date = pd.Timestamp(shock_date)

    rows = []
    for col in shocked_returns.columns:
        metrics = drawdown_metrics(shocked_returns[col], shock_date=shock_date)
        metrics["scenario"] = col
        rows.append(metrics)

    summary = pd.DataFrame(rows).set_index("scenario")

    # make it nicer for reading: sort by max drawdown (most negative first)
    summary = summary.sort_values("max_drawdown")

    # convert drawdown to percentage for readability
    summary["max_drawdown_pct"] = 100 * summary["max_drawdown"]

    # optional: drop the fractional version for a cleaner table
    summary = summary.drop(columns=["max_drawdown"])

    # reorder columns so max_drawdown_pct sits where max_drawdown was
    desired_order = [
    "shock_date",
    "pre_shock_level",
    "max_drawdown_pct",
    "max_drawdown_date",
    "recovery_date",
    "days_to_recovery",
    ]

    summary = summary[desired_order]

    return summary
