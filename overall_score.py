class OverallScore:

    def calculate(
        self,
        technical,
        quality,
        dividend
    ):

        return round(

            technical * 0.40 +

            quality * 0.40 +

            dividend * 0.20,

            1

        )

    def rating(self, score):

        if score >= 85:
            return "STRONG BUY"

        if score >= 75:
            return "BUY"

        if score >= 60:
            return "WATCH"

        return "IGNORE"