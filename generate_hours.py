import time
import random
import datetime

import numpy as np

from conf import *

#####
# FUNCS
#####


def increase_hours(array, hours):
    remaining_hours = hours - np.sum(array)
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
    remaining_hours = np.sum(array) - hours
    for j in range(max_hours):
        if remaining_hours <= 0:
            break

        for i in range(len(array)):
            if remaining_hours <= 0:
                break
            if array[i] > min_hours:
                array[i] = max(array[i] - 1, min_hours)
                remaining_hours -= 1


def match_sum(array, hours):
    array[array < hours_threshold] = 0
    if np.sum(array) < hours:
        increase_hours(array, hours)
    elif np.sum(array) > hours:
        decrease_hours(array, hours)


def random_hours_dirichlet(days, hours) -> np.ndarray:
    alphas = np.ones(days)
    weights = np.random.dirichlet(alphas)
    result = np.clip(weights * hours, min_hours, max_hours)
    match_sum(result, hours)

    return result


def generate_monthly_hours(array):
    days = (array != 0).sum()
    hours = hours_each_month - (array.sum() + (array == -1).sum())
    random_array = random_hours_dirichlet(days, hours)

    embedded_random_array = np.zeros_like(array)
    embedded_random_array[array != 0] = random_array

    array[array == -1] = 0
    array += embedded_random_array
    array = np.clip(array, min_hours, max_hours)

    result = array[array != 0]
    match_sum(result, hours_each_month)
    array[array != 0] = result

    return array


def generate_hours(days) -> np.ndarray:
    result = [
        np.zeros(31),  # January
        np.zeros(28),  # February (ignoring leap years)
        np.zeros(31),  # March
        np.zeros(30),  # April
        np.zeros(31),  # May
        np.zeros(30),  # June
        np.zeros(31),  # July
        np.zeros(31),  # August
        np.zeros(30),  # September
        np.zeros(31),  # October
        np.zeros(30),  # November
        np.zeros(31),  # December
    ]
    if days_in_year() == 366:
        result[1] = np.zeros(29)

    for m in range(len(result)):
        for d in range(len(result[m])):
            date = datetime.date(year, m + 1, d + 1)
            c_day = get_current_day_from_date(date)

            if not start_date <= date <= end_date:
                continue

            if is_event_day(c_day):
                result[m][d] = get_event_day_hour(c_day)
            elif is_working_day(c_day):
                result[m][d] = -1
        result[m] = generate_monthly_hours(result[m])
    return result


def write_output_file(filename, hours):
    with open(filename, "w") as f:
        for m in range(len(hours)):
            for d in range(len(hours[m])):
                date = datetime.date(year, m + 1, d + 1)
                output = f"{date.month},{date.day},{hours[m][d]}#{weekday_map[get_weekday(date)]}\n"
                f.write(output)


def convert_info_to_dict(result_hours, days) -> dict:
    info = {
        "expected_hours": int(hours_each_month * number_of_work_months),
        "actual_hours": round(sum([x.sum() for x in result_hours])),
        "expected_workdays": days * number_of_work_months / 12,
        "actual_workdays": sum([(x != 0).sum() for x in result_hours]),
        "black_days": int(52 * len(black_days) * number_of_work_months / 12),
        "event_days": int(52 * len(event_days) * number_of_work_months / 12),
        "expected_max_hours": max_hours,
        "actual_max_hours": round(max([x.max() for x in result_hours]), 3),
        "expected_min_hours": min_hours,
        "actual_min_hours": round(min([x[x > 0].min(initial=max_hours) for x in result_hours]), 3),
        "threshold": hours_threshold,
    }
    return info


def main() -> dict:
    days = int(days_in_year() * (7 - len(black_days)) / 7)

    result_hours = generate_hours(days)
    write_output_file("generated_hours.txt", result_hours)

    return convert_info_to_dict(result_hours, days)


if __name__ == "__main__":
    info = main()

    print(info)
    print("Hours generated\n\n")
