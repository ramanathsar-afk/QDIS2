import subprocess
import time
from datetime import datetime


RUN_HOUR = 7
RUN_MINUTE = 0


def run_qdis():

    print(f"\n{datetime.now():%Y-%m-%d %H:%M:%S}")

    subprocess.run(["python", "app.py"])


def main():

    print("QDIS Scheduler Started")

    last_run = None

    while True:

        now = datetime.now()

        if (
            now.hour == RUN_HOUR
            and now.minute == RUN_MINUTE
            and last_run != now.date()
        ):

            run_qdis()

            last_run = now.date()

        time.sleep(30)


if __name__ == "__main__":

    main()