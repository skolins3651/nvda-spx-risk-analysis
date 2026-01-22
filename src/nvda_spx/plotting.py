from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def plot_cumulative(
    returns: pd.DataFrame,
    title: str = "Cumulative Growth of $1",
    annotations: dict[str | pd.Timestamp, str] | None = None,
):
    """
    Plot cumulative growth of $1 for one or more return series.
    If returns are simple returns r_i, then cumulative growth is computed as:
    Growth_t = (1 + r_1) * (1 + r_2) * ... * (1 + r_t) = cumprod(1 + r_i)
    We use "growth of $1" for interpretability.

    Parameters
    ----------
    returns : pd.DataFrame
        Each column is a return series (simple returns).
    title : str
        Plot title.
    annotations : dict[date, label] | None
        Optional vertical line markers with labels.
    """
    growth = (1 + returns).cumprod()

    ax = growth.plot(figsize=(10, 5))
    ax.set_title(title)
    ax.set_ylabel("Growth of $1")
    ax.grid(True, alpha=0.3)

    if annotations:
        for dt, label in annotations.items():
            dt = pd.Timestamp(dt)
            ax.axvline(dt, linestyle="--", alpha=0.5)
            # place label near the top of the plot
            ax.text(
                dt,
                ax.get_ylim()[1],
                f" {label}",
                rotation=90,
                verticalalignment="top",
                fontsize=9,
                alpha=0.7,
            )

    return ax

def rolling_beta(
    y: pd.Series,
    x: pd.Series,
    window: int = 60,
) -> pd.Series:
    """
    Rolling beta of y on x computed as Cov(y, x) / Var(x). Default window is 60 trading days.
    """
    # align x,y on dates, drop NA's *after* pairing (all to prevent silent misalignments)
    df = pd.concat({"y": y, "x": x}, axis=1).dropna()

    # computes (co)variance of y with x on rolling window
    cov = df["y"].rolling(window).cov(df["x"])
    var = df["x"].rolling(window).var()

    beta = cov / var
    beta.name = f"beta_{y.name}_on_{x.name}"
    return beta

def plot_rolling_beta(
    y: pd.Series,
    x: pd.Series,
    window: int = 60,
    title: str | None = None,
):
    """
    Plot rolling beta of y on x. Adds regime shading to contextualize beta values:
    0-0.05: very low beta (marginal influence, gray region)
    0.05-0.1: moderate beta (influential, blue region)
    0.1-0.15: high beta (strong influence, orange region)
    >0.15: very high beta (dominant/systemic influence, red region)
    """
    beta = rolling_beta(y, x, window=window)

    ax = beta.plot(figsize=(10, 4))
    ax.set_title(title or f"Rolling Beta (window={window})")
    ax.set_ylabel("Beta")
    ax.grid(True, alpha=0.3)

    # regime shading
    ax.axhspan(0.00, 0.05, color="gray", alpha=0.1, label="Marginal")
    ax.axhspan(0.05, 0.10, color="blue", alpha=0.1, label="Influential")
    ax.axhspan(0.10, 0.15, color="orange", alpha=0.1, label="Strong")
    ax.axhspan(0.15, 1.00, color="red", alpha=0.1, label="Systemic")

    ax.legend(loc="upper right")

    return ax

def plot_rolling_beta_windows(
    y: pd.Series,
    x: pd.Series,
    windows: list[int],
    title: str | None = None,
):
    """
    Plot rolling beta of y on x for multiple window lengths in stacked subplots
    with shared axes and regime shading.
    """
    if not windows:
        raise ValueError("windows must be a non-empty list of integers.")

    fig, axes = plt.subplots(
        nrows=len(windows),
        ncols=1,
        figsize=(10, 3 * len(windows)),
        sharex=True,
        sharey=True,
    )

    # if there's only one window, axes is a single Axes object; normalize to list
    if len(windows) == 1:
        axes = [axes]

    betas = []
    for ax, w in zip(axes, windows):
        beta = rolling_beta(y, x, window=w)
        betas.append(beta)

        beta.plot(ax=ax)
        ax.set_title(f"Rolling Beta (window={w})")
        ax.set_ylabel("Beta")
        ax.grid(True, alpha=0.3)

        # regime shading (same as plot_rolling_beta)
        ax.axhspan(0.00, 0.05, color="gray", alpha=0.1, label="Marginal")
        ax.axhspan(0.05, 0.10, color="blue", alpha=0.1, label="Influential")
        ax.axhspan(0.10, 0.15, color="orange", alpha=0.1, label="Strong")
        ax.axhspan(0.15, 1.00, color="red", alpha=0.1, label="Systemic")

    if title:
        fig.suptitle(title)

    # put a single legend on the top subplot (avoid repeating)
    axes[0].legend(loc="upper right")

    fig.tight_layout()

    return fig, axes
