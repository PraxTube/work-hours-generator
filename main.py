import time
import random

import numpy as np
from openpyxl.reader.excel import load_workbook

#####
# CONSTS
#####

input_file = "zeitbogen.xlsx"
output_file = "output.xlsx"

name = "Klausius Mausius"
hours_each_week = 11
days_each_week = 5
department = "CLOWN SCHOOL"

days_in_year = 365

#####
# VARS
#####

# Both of the following refer to working days only
max_hours_a_day = 6
min_hours_a_day = 0
# Both of the following are in hours and refer to working days only
earliest_time = 8
latest_time = 20

#####
# GLOBALS
#####

current_day = 0

#####
# UTILS
#####

def format_time(hours) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(3600 * hours))


def is_working_day(day:str) -> bool:
    return day != ""

#####
# FUNCS
#####

def set_header_data(sheet):
    sheet.cell(row=3, column=5).value = name
    sheet.cell(row=3, column=10).value = department
    sheet.cell(row=4, column=2).value = hours_each_week
    sheet.cell(row=4, column=5).value = days_each_week
    sheet.cell(row=4, column=7).value = format_time(hours_each_week / days_each_week) 


def set_hours(sheet, hours):
    cell = (7, 3)
    day = sheet.cell(cell[0], cell[1] - 2).value
    print(current_day)
    while day != "":
        if current_day > len(hours):
            raise ValueError("Not enough values in 'hours' to fill the file.")
        if is_working_day(day):
            sheet.cell(cell[0], cell[1]).value = format_time(hours[current_day])
            #print(sheet.cell(cell[0], cell[1]))
        current_day += 1

        cell = (cell[0] + 1, cell[1])
        day = sheet.cell(cell[0], cell[1] - 2).value


def increase_hours(array, hours, mi, ma):
    remaining_hours = hours - sum(array)
    for j in range(ma):
        if remaining_hours <= 0:
            break

        for i in range(len(array)):
            if remaining_hours <= 0:
                break
            if array[i] < ma:
                array[i] += 1
                remaining_hours -= 1


def decrease_hours(array, hours, mi, ma):
    remaining_hours = hours - sum(array)
    for j in range(ma):
        if remaining_hours <= 0:
            break

        for i in range(len(array)):
            if remaining_hours <= 0:
                break
            if array[i] > mi:
                array[i] -= 1
                remaining_hours -= 1


def random_hours_dirichlet(days, hours, mi, ma) -> list:
    alphas = np.ones(days)
    weights = np.random.dirichlet(alphas)
    unbound =  [int(round(w * hours)) for w in weights]
    result = [min(ma, max(mi, x)) for x in unbound]

    return result


def generate_hours() -> list:
    days = int(days_in_year * days_each_week / 7)
    hours = int(days_in_year * hours_each_week / 7)
    mi, ma = min_hours_a_day, max_hours_a_day

    print(days)
    print(hours)

    result = random_hours_dirichlet(days, hours, mi, ma)

    if sum(result) < hours:
        increase_hours(result, hours, mi, ma)
    elif sum(result) > hours:
        decrease_hours(result, hours, mi, ma)

    return result



def main():
    hours = generate_hours()
    print(current_day)
    wb = load_workbook(input_file)
    for sheet in wb.worksheets:
        set_header_data(sheet)
        set_hours(sheet, hours)
    wb.save(output_file)


if __name__ == "__main__":
    main()

