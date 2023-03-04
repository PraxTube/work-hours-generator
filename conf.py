import datetime

#####
# CONSTS
#####

raw_data_input_file = "generated_hours.txt"
xlsx_input_file = "zeitbogen.xlsx"
xlsx_output_file = "output.xlsx"

name = "UNKO YAROU"
department = "TU BERLIN"
hours_each_month = 60
black_days = [0, 1, 2]
days_each_week = 7 - len(black_days)

year = 2021
# Both of the following refer to working days only
max_hours = 6
min_hours = 0
# This will make sure that the hours are rounded.
# For the value 12, this will mean that all: minutes % 5 = 0
round_hour_by = 6
start_hour = 10

weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

#####
# UTILS
#####

def is_working_day(current_day:int) -> bool:
    date = get_date_from_current_day(current_day)

    if get_weekday(date) in black_days:
        return False
    return True


def get_date_from_current_day(current_day:int) -> datetime.date:
    return datetime.date(year, 1, 1) + datetime.timedelta(days=current_day)


def get_weekday(date:datetime.date) -> int:
    return datetime.datetime(date.year, date.month, date.day).weekday()


def format_time(hours:float) -> str:
    return seconds_to_time(int(3600 * hours))


def seconds_to_time(seconds:int):
    time_delta = datetime.timedelta(seconds=seconds)

    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return datetime.time(hour=hours, minute=minutes)


def days_in_year() -> int:
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    return (last_day - first_day).days + 1

