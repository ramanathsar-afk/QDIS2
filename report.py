from pathlib import Path
from datetime import datetime

import pandas as pd


class Report:

    def __init__(self):

        self.folder = Path("reports")

        self.folder.mkdir(exist_ok=True)

    # --------------------------------------------------

    def save(self, df):

        if df.empty:

            print("No report to save.")

            return None

        df = df.sort_values(
            "Overall",
            ascending=False
        ).reset_index(drop=True)

        df.insert(0, "Rank", range(1, len(df) + 1))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        excel = self.folder / f"QDIS_Report_{timestamp}.xlsx"

        csv = self.folder / f"QDIS_Report_{timestamp}.csv"

        with pd.ExcelWriter(
            excel,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="QDIS"
            )

            ws = writer.sheets["QDIS"]

            for column in ws.columns:

                length = max(
                    len(str(c.value))
                    if c.value is not None
                    else 0
                    for c in column
                )

                ws.column_dimensions[
                    column[0].column_letter
                ].width = min(length + 2, 40)

        df.to_csv(csv, index=False)

        print(f"\nExcel : {excel}")

        print(f"CSV   : {csv}")

        return excel