import pandas as pd

from technical_score import TechnicalScore
from quality import QualityScore
from dividend import DividendScore
from overall_score import OverallScore


class Scanner:

    def __init__(self):

        self.technical = TechnicalScore()
        self.quality = QualityScore()
        self.dividend = DividendScore()
        self.overall = OverallScore()

    # --------------------------------------------------

    def scan(self, indicators_df, fundamentals_df):

        latest = (
            indicators_df
            .sort_values(["Symbol", "Date"])
            .groupby("Symbol")
            .tail(1)
        )

        fundamentals = fundamentals_df.set_index("Symbol")

        results = []

        for _, row in latest.iterrows():

            symbol = row["Symbol"]

            if symbol not in fundamentals.index:
                continue

            f = fundamentals.loc[symbol]

            technical = self.technical.calculate(row)

            quality = self.quality.calculate(f)

            dividend = self.dividend.calculate(f)

            overall = self.overall.calculate(
                technical,
                quality,
                dividend,
            )

            rating = self.overall.rating(overall)

            # Dividend Yield (%)

            dy = None

            if pd.notna(f["DividendYield"]):

                dy = float(f["DividendYield"])

                if dy <= 1:
                    dy *= 100

                dy = round(dy, 2)

            results.append({

                "Symbol": symbol,

                "Close": round(row["Close"], 2),

                "Technical": technical,

                "Quality": quality,

                "Dividend": dividend,

                "Overall": overall,

                "Rating": rating,

                "ADX": round(row["ADX14"], 1),

                "RSI": round(row["RSI14"], 1),

                "Drop90": round(row["Drop90"], 1),

                "DividendYield": dy,

                "PE": round(
                    f["PE"],
                    2
                ) if pd.notna(f["PE"]) else None,

                "ROE": round(
                    f["ROE"] * 100,
                    1
                ) if pd.notna(f["ROE"]) else None,

            })

        report = pd.DataFrame(results)

        if report.empty:
            return report

        report = report.sort_values(
            "Overall",
            ascending=False
        ).reset_index(drop=True)

        return report