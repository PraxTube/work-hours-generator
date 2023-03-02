#####
# CONSTS
#####

raw_data_input_file = "generated_hours.txt"
xlsx_input_file = "zeitbogen.xlsx"
xlsx_output_file = "output.xlsx"

name = "UNKO YAROU"
department = "TU BERLIN"
hours_each_week = 15
black_days = [5, 6]
days_each_week = 7 - len(black_days)

year = 2023
# Both of the following refer to working days only
max_hours = 6
min_hours = 0
# This will make sure that the hours are rounded.
# For the value 12, this will mean that all: minutes % 5 = 0
round_hour_by = 6
start_hour = 10

weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

