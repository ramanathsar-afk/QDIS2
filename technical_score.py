class TechnicalScore:

    def calculate(self, row):

        score = 0

        # --------------------------------
        # Moving Average Alignment
        # --------------------------------

        if (
            row["MA21"] >
            row["MA50"] >
            row["MA100"] >
            row["MA200"]
        ):
            score += 25

        # --------------------------------
        # Positive Slopes
        # --------------------------------

        positive = sum([
            row["MA21_Slope"] > 0,
            row["MA50_Slope"] > 0,
            row["MA100_Slope"] > 0,
            row["MA200_Slope"] > 0
        ])

        score += positive * 5

        # --------------------------------
        # ADX
        # --------------------------------

        adx = row["ADX14"]

        if adx >= 40:
            score += 20
        elif adx >= 30:
            score += 15
        elif adx >= 25:
            score += 10

        # --------------------------------
        # RSI
        # --------------------------------

        rsi = row["RSI14"]

        if 45 <= rsi <= 65:
            score += 10

        # --------------------------------
        # Pullback from High90
        # --------------------------------

        drop = abs(row["Drop90"])

        if drop >= 30:
            score += 25
        elif drop >= 20:
            score += 20
        elif drop >= 15:
            score += 15
        elif drop >= 10:
            score += 10

        return min(score, 100)