import time
import random
import datetime

import numpy as np
from openpyxl.reader.excel import load_workbook

import generate_hours
import generate_xlsx


def print_msg(msg, actual_val, expected_val):
    print("{}: {} / {}".format(msg, actual_val, expected_val))


def print_info_hours(info):
    print("\nThe following ratios are 'actual_val/expected_val':\n")

    print_msg("Total sum of hours", info["actual_hours"], info["expected_hours"])
    print_msg(
        "Total sum of workdays", info["actual_workdays"], info["expected_workdays"]
    )
    print_msg(
        "Amount of black days to work days", info["black_days"], info["actual_workdays"]
    )
    print_msg(
        "Amount of event days to work days", info["event_days"], info["actual_workdays"]
    )
    print_msg("Max hours worked", info["actual_max_hours"], info["expected_max_hours"])
    print_msg(
        "Min hours worked (non-zero)",
        info["actual_min_hours"],
        info["expected_min_hours"],
    )
    print_msg(
        "Threshold hours", info["actual_min_hours"], info["threshold"]
    )


def print_info_xlsx(info):
    print("")

    print("Total hours in the xlsx file: {}".format(info["total_hours"]))
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Mai",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    for i in range(len(months)):
        diff = round(info["monthly_hours"][i] - info["expected_month_hour"][i])

        sign = "-" if diff < 0 else "+"
        print(
            "{}: {}, {} {}".format(months[i], info["monthly_hours"][i], sign, abs(diff))
        )
    print("Start date: {}".format(info["start_date"]))
    print("End date:   {}".format(info["end_date"]))


def main():
    info_hours = generate_hours.main()
    info_xlsx = generate_xlsx.main()

    print_info_hours(info_hours)
    print_info_xlsx(info_xlsx)


if __name__ == "__main__":
    main()
