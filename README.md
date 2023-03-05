# Work Hours Generator

Generate random work hours from a given start date to an end date output the result in a xlsx file.

## Table of Contents

[Installation](#installation) <br>
[Usage](#usage) <br>
[Examples](#examples) <br>
[Notes on the xlsx output file](#notes-on-the-xlsx-output-file) <br>
[Output of main.py](#output-of-main.py) <br>
[Warnings and edge cases](#warnings-and-edge-cases) <br>
[Further customization](#further-customization) <br>

## Installation

An installed version of python is required as well as the python libraries inside of
`requirements.txt`.

To install and use this repo, run the following commands

```
git clone https://github.com/PraxTube/work-hours-generator.git
cd work-hours-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Now you can run

```
python main.py
```

to see that everything worked.

## Usage

The usage of this repo is pretty straightforward:

1. Configure the settings inside of `conf.py`
2. Run the command `python main.py`

### Configuring `conf.py`

The way to costumize your generation is by changing the values in the python script `conf.py`.

The **Basic** settings:

```
name - Your name
department - Your working department
hours_each_month - How many hours you work each month
year - The year to generate hours for
start_date - The date to start generating hours from
end_date - The date to stop generating hours to
max_hours - The maximum amount of hours workdays can have
min_hours - The minimum amount of hours workdays should hve
```

Most of them are self-explanatory, however, it should be noted that `max_hours` and `min_hours` only apply to **workdays**,
this means if you set `min_hours=1`, only the workdays will have at least 1 hours, **not** all days.

Workdays in this context refer to days that can have `hours>=0`. If a day is a workday or not depends on the specified `black_days` and `event_days`, see below.

The **Advanced** settings:

```
black_days - list, Mark specific days as non workdays
event_days - dict, Mark specific days as eventdays, great for simulating meetings
hours_threshold - float in [0, 1], Any workdays below this value will be set to 0
round_hours_by - int, Rounds all work hours: round(hours / round_hours_by) * round_hours_by
```

For more info on these settings, see the `conf.py` file and the examples below.

## Examples

The following section will provide some examples for setting a `conf.py` file.

If you wish to only generate hours from Mon - Fri with a meeting on every Mon that goes for 2 hours, then you can use

```
# Black lists Sat and Sun
black_days = [5, 6]
# Every Mon will have at least 2 hours
event_days = {"0": 2.0}
```

Rounding and thresholding your hours can be achieved by setting

```
# Will make sure all hours are >=30 minutes
hours_theshold = 0.5
# Will round all hours so that the minutes are multiple of 10
round_hours_by = 6
```

note that `hours_threshold` should be in between `[0, 1]`. If the value is `>1` it can cause issues with the generation process.
The rounding makes sure that all hours displayed in the xlsx file have a minute count of `n * 60 / round_hours_by`. Note that this can cause a deviation on your
total hours, so always make sure to check the print output and the xlsx file to check the amount of hours generated. Also note, because of float inprecision, the rounding can be off by a minute.

Generating hours from a certain date to another certain date (as opposed to generting hours for the whole year), can be achieved by setting

```
year = 2022
start_date = datetime.date(year, 3, 15)
end_date = datetime.date(year, 8, 31)
```

which in this case, will generate hours from the 15th March to the 31th August. The current implementation will try to fit your monthly hours in any month,
meaning that it will attempt to fill March in this case with the same amount of hours as any other month. In general, if you wish to generate from specific dates,
a little bit of manual work is still needed. Leap years are being accounted for.

You can also create the hours completely manually by setting

```
# Black list all days
black_days = [0, 1, 2, 3, 4, 5, 6]
# Use the event days to manually set all hours
event_days = {"0": 2.0, "1": 3.0, "2": 5.5, "6": 2.0}
```

which will set **only** the event days and not generate any other hours (note that the program will still try to clip the hour values in between
`min_hours` and `max_hours`, and also try to increase/decrease the hours to your monthly hours).

## Notes on the xlsx output file

The xlsx output file is very barebones and does not have a lot of funtionality. The things it does do automatically:

- Format the weekday (cells in `A`) and date (cells in `B`) according to the date set in the header
- Calculate the sum of the hours worked each month minus expected hours (cell `C38`)
- Calculate the sum of all hours minus all expected hours (last sheet cell `C38`)

The user doesn't need to interact with the xlsx file directly, unless you set `start_date` or `end_date`, in this case you may need to set the monthly hours in cell `B4`.

The rounding of the numbers can also be a inaccurate.

## Output of main.py

The following is an example output when `python main.py` is run

```
The following ratios are 'actual_val/expected_val':

Total sum of hours: 723 / 720
Total sum of workdays: 231 / 260
Amount of black days to work days: 104 / 231
Amount of event days to work days: 52 / 231
Max hours worked: 6.0 / 6
Min hours worked (non-zero): 0.508 / 0
Threshold hours: 0.508 / 0.5

Total hours in the xlsx file: 723
Jan: 60, + 0
Feb: 60, + 0
Mar: 59, - 1
Apr: 61, + 1
Mai: 61, + 1
Jun: 60, + 0
Jul: 61, + 1
Aug: 59, - 1
Sep: 60, + 0
Oct: 61, + 1
Nov: 60, + 0
Dec: 60, + 0
Start date: 2022-01-01
End date:   2022-12-31
```

Most of the output is self-explanatory. The `sum of workdays` refers to days where the number
of hours is `>0`. The number behind each month represents how many hours of work it contains
and the difference behind it states how much it deviates from the set amount of hours.

In general it is still best to open the xlsx file and go through a few sheets to make sure
the generation process was successful.

## Warnings and edge cases

There are almost no checks or warnings in any of the scripts (as of now). The best way to avoid
problems is to be aware of the edge cases listed below and to check your outpur of `main.py`.

Following edge cases will potentially create errors in the generation process:

- black listing too many days
- setting `max_hour` too low
- setting `hours_threshold` too high
- setting `round_hours_by` to a weird number (should be kept in `[1, 60]`)
- setting `min_hour >= max_hour`

The output of `main.py` is generally a good indicator to see if the generation went well, in particular
the actual and expected hours.

## Further customization

In case you wish to costumize your generation even further, here are some tips for you.

### Hour generation

The hours get generated in the `generate_hours.py`, which writes its output to `generated_hours.txt`.
In order to costumize it, you could write a whole new script from scratch and use the same output format
as the current `generated_hours.txt`, whish would allow you to still use `generate_xlsx.py` to generate the
final xlsx file.

### Xlsx generation

If you wish to change the generation of the xlsx file, then you want to modify `generate_xlsx.py`, which reads
from `generated_hours.txt`. You would only really need to modify `generate_xlsx.py` if you would use a different
xlsx file. If you only care about the hour generation then you don't need to change anything about the
`generate_xlsx.py` file.

Feel free to contribute to this repo.
