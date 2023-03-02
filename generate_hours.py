import time
import random
import datetime

import numpy as np

from conf import *

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


def days_in_year() -> int:
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    return (last_day - first_day).days + 1

#####
# FUNCS
#####

def increase_hours(array, hours):
    remaining_hours = hours - sum(array)
    for j in range(max_hours):
        if remaining_hours <= 0:
            break

        for i in range(len(array)):
            if remaining_hours <= 0:
                break
            if array[i] < max_hours:
                array[i] += 1
                remaining_hours -= 1


def decrease_hours(array, hours):
    remaining_hours = hours - sum(array)
    for j in range(max_hours):
        if remaining_hours <= 0:
            break

        for i in range(len(array)):
            if remaining_hours <= 0:
                break
            if array[i] > min_hours:
                array[i] -= 1
                remaining_hours -= 1


def random_hours_dirichlet(days, hours) -> np.ndarray:
    alphas = np.ones(days)
    weights = np.random.dirichlet(alphas)
    result = np.clip(weights * hours, min_hours, max_hours)

    return result


def generate_hours(days, hours) -> np.ndarray:
    """Generate hours in an array with length days

    The result will have clamped values between mi and ma
    """
    result = random_hours_dirichlet(days, hours)

    if sum(result) < hours:
        increase_hours(result, hours)
    elif sum(result) > hours:
        decrease_hours(result, hours)

    return result


def write_output_file(filename, hours):
    with open(filename, 'w') as f:
        for i in range(days_in_year()):
            if not is_working_day(i):
                continue

            if i >= len(hours):
                continue

            date = get_date_from_current_day(i)
            output = f"{date.month},{date.day},{hours[i]}#{weekday_map[get_weekday(date)]}\n"
            f.write(output)
    

def main():
    days = int(days_in_year() * 7 / (7 - len(black_days)))
    hours = hours_each_week * 52

    result_hours = generate_hours(days, hours)
    write_output_file("generated_hours.txt", result_hours)

    print("\n\nDone")


if __name__ == "__main__":
    main()

