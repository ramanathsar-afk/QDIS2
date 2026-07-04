class DividendScore:

    def calculate(self, f):

        score = 0

        # Dividend Yield

        y = f["DividendYield"]

        if y is not None:

            if y >= 0.06:
                score += 35
            elif y >= 0.04:
                score += 25
            elif y >= 0.03:
                score += 15
            elif y >= 0.02:
                score += 10

        # Payout Ratio

        p = f["PayoutRatio"]

        if p is not None:

            if 0.30 <= p <= 0.60:
                score += 35
            elif 0.20 <= p <= 0.70:
                score += 25
            elif 0.10 <= p <= 0.80:
                score += 15

        # Dividend Rate

        r = f["DividendRate"]

        if r is not None:

            if r > 2:
                score += 30
            elif r > 1:
                score += 20
            elif r > 0:
                score += 10

        return score