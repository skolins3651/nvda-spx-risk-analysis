from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def plot_cumulative(
    returns: pd.DataFrame,
    title: str = "Cumulative Growth of $1",
):
    """
    Plot cumulative growth of $1 for one or more return series.
    If returns are simple returns r_i, then cumulative growth is computed as:
    Growth_t = (1 + r_1) * (1 + r_2) * ... * (1 + r_t) = cumprod(1 + r_i)
    We use "growth of $1" for interpretability.
    """
    growth = (1 + returns).cumprod()

    ax = growth.plot(figsize=(10, 5))
    ax.set_title(title)
    ax.set_ylabel("Growth of $1")
    ax.grid(True, alpha=0.3)

    return ax
