from __future__ import annotations # allows for free use of type hints without runtime issues

from typing import Optional
import pandas as pd
import yfinance as yf

def download_prices(spx_ticker: str, 
                    nvda_ticker: str,
                    start_date: str,
                    end_date: Optional[str] = None,
                    ) -> pd.DataFrame:
    """
    Download daily prices for SPX and NVDA and return a DataFrame with columns:
    ['SPX', 'NVDA'] indexed by date.

    We use auto_adjust=True so the prices are adjusted for splits/dividends
    (important for long-horizon return analysis).
    """
    tickers = [spx_ticker, nvda_ticker]

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    close = data["Close"].copy() # only need closing prices
    close = close.rename(columns={spx_ticker: "SPX", nvda_ticker: "NVDA"})
    close = close.dropna() # drop any rows with missing data
    return close





