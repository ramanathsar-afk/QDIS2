from database import Database
from downloader import Downloader
from indicators import Indicators
from fundamentals import Fundamentals
from scanner import Scanner
from report import Report

from config import WATCHLIST

from datetime import datetime
import pandas as pd


def load_watchlist():

    df = pd.read_csv(WATCHLIST)

    return df.iloc[:, 0].dropna().tolist()


# ------------------------------------------------------


def save_indicators(db, symbol, df):

    rows = []

    for _, r in df.iterrows():

        rows.append(
            (
                symbol,
                r["Date"],
                r["MA21"],
                r["MA50"],
                r["MA100"],
                r["MA200"],
                r["ATR14"],
                r["ADX14"],
                r["RSI14"],
                r["MA21_Slope"],
                r["MA50_Slope"],
                r["MA100_Slope"],
                r["MA200_Slope"],
                r["High30"],
                r["High60"],
                r["High90"],
                r["High180"],
                r["High252"],
                r["Drop30"],
                r["Drop60"],
                r["Drop90"],
                r["Drop180"],
                r["Drop252"],
            )
        )

    db.executemany(
        """
        INSERT OR REPLACE INTO Indicators
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        rows,
    )


# ------------------------------------------------------


def save_fundamentals(db, data):

    db.execute(
        """
        INSERT OR REPLACE INTO Fundamentals
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            data["Symbol"],
            data["DividendYield"],
            data["DividendRate"],
            data["PayoutRatio"],
            data["MarketCap"],
            data["PE"],
            data["ForwardPE"],
            data["EPS"],
            data["BookValue"],
            data["PriceToBook"],
            data["Beta"],
            data["ROE"],
            data["ProfitMargins"],
            data["OperatingMargins"],
            data["RevenueGrowth"],
            data["EarningsGrowth"],
            datetime.now().strftime("%Y-%m-%d"),
        ),
    )


# ------------------------------------------------------


def main():

    db = Database()

    downloader = Downloader()

    indicators = Indicators()

    fundamentals = Fundamentals()

    scanner = Scanner()

    report_writer = Report()

    symbols = load_watchlist()

    print(f"\nProcessing {len(symbols)} stocks\n")

    for symbol in symbols:

        print(symbol)

        df = downloader.download(symbol)

        if df.empty:
            continue

        # -------------------------
        # Prices
        # -------------------------

        price_rows = []

        for _, r in df.iterrows():

            price_rows.append(
                (
                    symbol,
                    r["Date"],
                    r["Open"],
                    r["High"],
                    r["Low"],
                    r["Close"],
                    r["AdjClose"],
                    r["Volume"],
                    r["Dividends"],
                    r["StockSplits"],
                )
            )

        db.executemany(
            """
            INSERT OR REPLACE INTO DailyPrices
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            price_rows,
        )

        # -------------------------
        # Indicators
        # -------------------------

        df = indicators.calculate(df)

        save_indicators(
            db,
            symbol,
            df,
        )

        # -------------------------
        # Fundamentals
        # -------------------------

        f = fundamentals.download(symbol)

        save_fundamentals(
            db,
            f,
        )

    # ===================================
    # Build Report
    # ===================================

    indicators_df = db.query(
        """
        SELECT
            i.*,
            p.Close
        FROM Indicators i
        JOIN DailyPrices p
          ON i.Symbol=p.Symbol
         AND i.Date=p.Date
        """
    )

    fundamentals_df = db.query(
        """
        SELECT *
        FROM Fundamentals
        """
    )

    report = scanner.scan(
        indicators_df,
        fundamentals_df,
    )

    print("\n")
    print(report)

    report_writer.save(report)

    db.close()

    print("\nQDIS Completed Successfully")


if __name__ == "__main__":

    main()