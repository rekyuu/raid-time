from datetime import datetime, timedelta
from flask import Flask, render_template
import random
from zoneinfo import ZoneInfo


SCHEDULE_MST = {
    "mon": None,
    "tue": (18.5, 21.5),
    "wed": (18.5, 21.0),
    "thu": None,
    "fri": (18.5, 21.5),
    "sat": None,
    "sun": None,
}


app = Flask(__name__)

MST_TZ = ZoneInfo("US/Mountain")
PST_TZ = ZoneInfo("US/Pacific")
UTC_TZ = ZoneInfo("UTC")


def _get_next_raid_time() -> int:
    now = datetime.now(MST_TZ)
    schedule_values = list(SCHEDULE_MST.values())

    days_i = -1
    weekday_i = now.weekday() - 1
    while days_i < 7:
        days_i += 1
        weekday_i += 1
        if weekday_i == 7:
            weekday_i = 0

        day = now + timedelta(days=days_i)
        schedule = schedule_values[weekday_i]
        if schedule is None:
            continue

        (start, end) = schedule

        (start_h, start_m) = divmod(start * 60, 60)
        start_dt = datetime(year=day.year, month=day.month, day=day.day, hour=int(start_h), minute=int(start_m),
                            tzinfo=MST_TZ)

        if start_dt > now:
            start_dt_utc = start_dt.astimezone(UTC_TZ)
            return int(start_dt_utc.timestamp())


def _get_pf_code() -> int:
    pst_now_date = datetime.now(tz=PST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    random.seed(pst_now_date.timestamp())

    return random.randint(0, 9999)


@app.route("/")
def index():
    return render_template("index.html",
                           next_raid_time=_get_next_raid_time(),
                           pf_code=_get_pf_code())


if __name__ == "__main__":
    app.run()
