from fundamentals import Fundamentals

f = Fundamentals()

data = f.download("BARC.L")

for k, v in data.items():

    print(f"{k:20} {v}")