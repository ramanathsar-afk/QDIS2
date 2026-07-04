import pandas as pd
import yfinance as yf

from config import HISTORY_YEARS


class Downloader:

    def download(self, symbol):

        ticker = yf.Ticker(symbol)

        df = ticker.history(
            period=f"{HISTORY_YEARS}y",
            auto_adjust=False
        )

        if df.empty:
            return df

        df = df.reset_index()

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

        rename = {}

        if "Stock Splits" in df.columns:
            rename["Stock Splits"] = "StockSplits"

        if "Adj Close" in df.columns:
            rename["Adj Close"] = "AdjClose"

        df.rename(columns=rename, inplace=True)

        required = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "AdjClose",
            "Volume",
            "Dividends",
            "StockSplits",
        ]

        for col in required:
            if col not in df.columns:
                df[col] = 0.0

        df = df[required]

        return df