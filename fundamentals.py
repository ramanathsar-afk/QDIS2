import pandas as pd
import yfinance as yf


class Fundamentals:

    def download(self, symbol):

        info = yf.Ticker(symbol).info

        return {

            "Symbol": symbol,

            "DividendYield": self.value(info, "dividendYield"),

            "DividendRate": self.value(info, "dividendRate"),

            "PayoutRatio": self.value(info, "payoutRatio"),

            "MarketCap": self.value(info, "marketCap"),

            "PE": self.value(info, "trailingPE"),

            "ForwardPE": self.value(info, "forwardPE"),

            "EPS": self.value(info, "trailingEps"),

            "BookValue": self.value(info, "bookValue"),

            "PriceToBook": self.value(info, "priceToBook"),

            "Beta": self.value(info, "beta"),

            "ROE": self.value(info, "returnOnEquity"),

            "ProfitMargins": self.value(info, "profitMargins"),

            "OperatingMargins": self.value(info, "operatingMargins"),

            "RevenueGrowth": self.value(info, "revenueGrowth"),

            "EarningsGrowth": self.value(info, "earningsGrowth")

        }

    def value(self, info, key):

        value = info.get(key)

        if value is None:

            return None

        return value