import numpy as np
import pandas as pd

from config import (
    MA_FAST,
    MA_MEDIUM,
    MA_SLOW,
    MA_LONG,
    ATR_PERIOD,
    ADX_PERIOD,
    RSI_PERIOD,
    SLOPE21,
    SLOPE50,
    SLOPE100,
    SLOPE200,
    HIGH_PERIODS,
)


class Indicators:

    def calculate(self, df):

        df = df.copy()

        # -------------------------
        # Moving Averages
        # -------------------------

        df["MA21"] = df["Close"].rolling(MA_FAST).mean()
        df["MA50"] = df["Close"].rolling(MA_MEDIUM).mean()
        df["MA100"] = df["Close"].rolling(MA_SLOW).mean()
        df["MA200"] = df["Close"].rolling(MA_LONG).mean()

        # -------------------------
        # ATR
        # -------------------------

        high_low = df["High"] - df["Low"]
        high_close = (df["High"] - df["Close"].shift()).abs()
        low_close = (df["Low"] - df["Close"].shift()).abs()

        tr = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        ).max(axis=1)

        df["ATR14"] = tr.rolling(ATR_PERIOD).mean()

        # -------------------------
        # RSI
        # -------------------------

        delta = df["Close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(RSI_PERIOD).mean()

        avg_loss = loss.rolling(RSI_PERIOD).mean()

        rs = avg_gain / avg_loss

        df["RSI14"] = 100 - (100 / (1 + rs))

        # -------------------------
        # ADX
        # -------------------------

        up = df["High"].diff()

        down = -df["Low"].diff()

        plus_dm = np.where(
            (up > down) & (up > 0),
            up,
            0,
        )

        minus_dm = np.where(
            (down > up) & (down > 0),
            down,
            0,
        )

        plus_di = (
            100
            * pd.Series(plus_dm)
            .rolling(ADX_PERIOD)
            .mean()
            / df["ATR14"]
        )

        minus_di = (
            100
            * pd.Series(minus_dm)
            .rolling(ADX_PERIOD)
            .mean()
            / df["ATR14"]
        )

        dx = (
            (
                (plus_di - minus_di).abs()
                / (plus_di + minus_di)
            )
            * 100
        )

        df["ADX14"] = dx.rolling(ADX_PERIOD).mean()

        # -------------------------
        # Normalised Slopes
        # -------------------------

        slope_map = {
            "MA21": SLOPE21,
            "MA50": SLOPE50,
            "MA100": SLOPE100,
            "MA200": SLOPE200,
        }

        for ma, bars in slope_map.items():

            df[f"{ma}_Slope"] = (
                (df[ma] - df[ma].shift(bars))
                / df["ATR14"]
            )

        # -------------------------
        # Highs / Drops
        # -------------------------

        for period in HIGH_PERIODS:

            df[f"High{period}"] = (
                df["Close"]
                .rolling(period)
                .max()
            )

            df[f"Drop{period}"] = (
                (
                    df["Close"]
                    - df[f"High{period}"]
                )
                / df[f"High{period}"]
                * 100
            )

        return df