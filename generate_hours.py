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


def generate_monthly_hours(monthly_days, month, hours):
    result = random_hours_dirichlet(monthly_days, hours)
    match_sum(result, hours_each_month)
    return result


def generate_hours(days) -> np.ndarray:
    monthly_days = days // 12
    result = np.zeros(12 * monthly_days).reshape(12, monthly_days)

    for i in range(12):
        result[i] += generate_monthly_hours(monthly_days, i, hours_each_month)
    remaining_days_result = random_hours_dirichlet(
        days % 12, max(0, 12 * hours_each_month - np.sum(result))
    )
    return np.concatenate((result.flatten(), remaining_days_result))


def write_output_file(filename, hours):
    start_index = get_current_day_from_date(start_date)
    end_index = get_current_day_from_date(end_date)
    remaining_hours = list(hours)

    with open(filename, "w") as f:
        for i in range(days_in_year()):
            if not is_working_day(i):
                continue

            if len(remaining_hours) <= 0:
                continue

            if i not in range(start_index, end_index + 1):
                remaining_hours.pop(0)
                continue

            date = get_date_from_current_day(i)
            output = f"{date.month},{date.day},{remaining_hours[0]}#{weekday_map[get_weekday(date)]}\n"
            remaining_hours.pop(0)
            f.write(output)


def convert_info_to_dict(result_hours, days) -> dict:
    info = {
        "expected_hours": 12 * hours_each_month,
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

    result_hours = generate_hours(days)
    write_output_file("generated_hours.txt", result_hours)

    return convert_info_to_dict(result_hours, days)


if __name__ == "__main__":
    info = main()

    print(info)
    print("Hours generated\n\n")
