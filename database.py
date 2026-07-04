import sqlite3
from pathlib import Path
import pandas as pd


class Database:

    def __init__(self, db_file="database/qdis.db"):

        self.db_file = Path(db_file)

        self.db_file.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_file)

        self.conn.row_factory = sqlite3.Row

        self.create_tables()

    # --------------------------------------------------

    def create_tables(self):

        c = self.conn.cursor()

        # ==============================================
        # Daily Prices
        # ==============================================

        c.execute("""
        CREATE TABLE IF NOT EXISTS DailyPrices(

            Symbol TEXT,

            Date TEXT,

            Open REAL,

            High REAL,

            Low REAL,

            Close REAL,

            AdjClose REAL,

            Volume REAL,

            Dividends REAL,

            StockSplits REAL,

            PRIMARY KEY(Symbol,Date)

        )
        """)

        # ==============================================
        # Indicators
        # ==============================================

        c.execute("""
        CREATE TABLE IF NOT EXISTS Indicators(

            Symbol TEXT,

            Date TEXT,

            MA21 REAL,
            MA50 REAL,
            MA100 REAL,
            MA200 REAL,

            ATR14 REAL,
            ADX14 REAL,
            RSI14 REAL,

            MA21_Slope REAL,
            MA50_Slope REAL,
            MA100_Slope REAL,
            MA200_Slope REAL,

            High30 REAL,
            High60 REAL,
            High90 REAL,
            High180 REAL,
            High252 REAL,

            Drop30 REAL,
            Drop60 REAL,
            Drop90 REAL,
            Drop180 REAL,
            Drop252 REAL,

            PRIMARY KEY(Symbol,Date)

        )
        """)

        # ==============================================
        # Fundamentals
        # ==============================================

        c.execute("""
        CREATE TABLE IF NOT EXISTS Fundamentals(

            Symbol TEXT PRIMARY KEY,

            DividendYield REAL,

            DividendRate REAL,

            PayoutRatio REAL,

            MarketCap REAL,

            PE REAL,

            ForwardPE REAL,

            EPS REAL,

            BookValue REAL,

            PriceToBook REAL,

            Beta REAL,

            ROE REAL,

            ProfitMargins REAL,

            OperatingMargins REAL,

            RevenueGrowth REAL,

            EarningsGrowth REAL,

            LastUpdated TEXT

        )
        """)

        # ==============================================
        # Watchlist
        # ==============================================

        c.execute("""
        CREATE TABLE IF NOT EXISTS Watchlist(

            Symbol TEXT PRIMARY KEY

        )
        """)

        self.conn.commit()

    # --------------------------------------------------

    def execute(self, sql, params=()):

        cur = self.conn.cursor()

        cur.execute(sql, params)

        self.conn.commit()

        return cur

    # --------------------------------------------------

    def executemany(self, sql, rows):

        cur = self.conn.cursor()

        cur.executemany(sql, rows)

        self.conn.commit()

    # --------------------------------------------------

    def query(self, sql, params=()):

        return pd.read_sql_query(sql, self.conn, params=params)

    # --------------------------------------------------

    def close(self):

        self.conn.close()