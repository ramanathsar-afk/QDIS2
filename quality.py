class QualityScore:

    def calculate(self, f):

        score = 0

        # -----------------------
        # ROE
        # -----------------------

        roe = f["ROE"]

        if roe is not None:

            if roe >= 0.20:
                score += 20
            elif roe >= 0.15:
                score += 15
            elif roe >= 0.10:
                score += 10
            elif roe >= 0.05:
                score += 5

        # -----------------------
        # Profit Margin
        # -----------------------

        pm = f["ProfitMargins"]

        if pm is not None:

            if pm >= 0.30:
                score += 20
            elif pm >= 0.20:
                score += 15
            elif pm >= 0.10:
                score += 10
            elif pm >= 0.05:
                score += 5

        # -----------------------
        # Operating Margin
        # -----------------------

        om = f["OperatingMargins"]

        if om is not None:

            if om >= 0.30:
                score += 20
            elif om >= 0.20:
                score += 15
            elif om >= 0.10:
                score += 10
            elif om >= 0.05:
                score += 5

        # -----------------------
        # Revenue Growth
        # -----------------------

        rg = f["RevenueGrowth"]

        if rg is not None:

            if rg >= 0.20:
                score += 20
            elif rg >= 0.10:
                score += 15
            elif rg >= 0.05:
                score += 10
            elif rg > 0:
                score += 5

        # -----------------------
        # Earnings Growth
        # -----------------------

        eg = f["EarningsGrowth"]

        if eg is not None:

            if eg >= 0.20:
                score += 20
            elif eg >= 0.10:
                score += 15
            elif eg >= 0.05:
                score += 10
            elif eg > 0:
                score += 5

        return score