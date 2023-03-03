import time
import random
import datetime

import numpy as np

from conf import *

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
                array[i] = min(array[i] + 1, max_hours)
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
                array[i] -= max(array[i] - 1, min_hours)
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
    remaining_hours = list(hours)

    with open(filename, 'w') as f:
        for i in range(days_in_year()):
            if not is_working_day(i):
                continue
            
            if len(remaining_hours) <= 0:
                continue

            date = get_date_from_current_day(i)
            output = f"{date.month},{date.day},{remaining_hours[0]}#{weekday_map[get_weekday(date)]}\n"
            remaining_hours.pop(0)
            f.write(output)
    

def convert_info_to_dict(result_hours, hours, days) -> dict:
    info = {
        "expected_hours": hours,
        "actual_hours": round(np.sum(result_hours)),
        "expected_workdays": days,
        "actual_workdays": len(result_hours),
        "expected_max_hours": max_hours,
        "actual_max_hours": round(np.max(result_hours), 3),
        "expected_min_hours": min_hours,
        "actual_min_hours": round(np.min(result_hours[np.nonzero(result_hours)]), 3),
    }
    return info


def main() -> dict:
    days = int(days_in_year() * (7 - len(black_days)) / 7)
    hours = hours_each_month * 12

    result_hours = generate_hours(days, hours)
    write_output_file("generated_hours.txt", result_hours)

    return convert_info_to_dict(result_hours, hours, days)


if __name__ == "__main__":
    info = main()

    print(info)
    print("Hours generated\n\n")

