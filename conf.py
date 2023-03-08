import datetime

#####
# CONSTS
#####

### BASICS ###

name = "Luka Rancic"
department = "SFB/TRR 109"
hours_each_month = 60

year = 2022
# Change the second entry (month) and the third (day)
start_date = datetime.date(year, 8, 26)
end_date = datetime.date(year, 11, 15)

max_hours = 6
min_hours = 0

### ADVANCED ###

# Values between 0 - 6, representing the weekdays, Mon = 0, Sun = 6
black_days = [6]
# Keys between 0 - 6, Values positive floats, i.e. "0": 2.0
event_days = {
    "0": 2,
}
# This makes sure all hours are above this threshold
# by setting the ones below to 0, should be between 0 - 1
hours_threshold = 0.5
# This will make sure that the hours are rounded.
# For the value 4, this means: 60 / 4 = 15
round_hour_by = 4

### DONT CHANGE ###

raw_data_input_file = "generated_hours.txt"
xlsx_input_file = "zeitbogen.xlsx"
xlsx_output_file = "output.xlsx"

days_each_week = 7 - len(black_days)

number_of_work_months = sum([1 if start_date.month <= x + 1 <= end_date.month else 0 for x in range(12)])

weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

#####
# UTILS
#####

def is_working_day(current_day: int) -> bool:
    date = get_date_from_current_day(current_day)

    if get_weekday(date) in black_days:
        return False
    return True


def is_event_day(current_day: int) -> bool:
    date = get_date_from_current_day(current_day)

    if str(get_weekday(date)) in event_days:
        return True
    return False


def get_event_day_hour(current_day: int) -> float:
    if not is_event_day(current_day):
        raise ValueError("The given day is NOT an event_day", current_day)

    date = get_date_from_current_day(current_day)
    index = get_weekday(date)
    return event_days[str(index)]


def get_date_from_current_day(current_day: int) -> datetime.date:
    return datetime.date(year, 1, 1) + datetime.timedelta(days=current_day)


def get_current_day_from_date(date: datetime.date) -> int:
    return (date - datetime.date(year, 1, 1)).days


def get_weekday(date) -> int:
    return datetime.datetime(date.year, date.month, date.day).weekday()


def format_time(hours: float) -> str:
    return seconds_to_time(int(3600 * hours))


def seconds_to_time(seconds: int):
    time_delta = datetime.timedelta(seconds=seconds)

    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return datetime.time(hour=hours, minute=minutes)


def days_in_year() -> int:
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    return (last_day - first_day).days + 1

