# Work Hours Generator

Generate random work hours in a given time frame and output the result in a xlsx file.

## Prerequisites

All that is required to use this repo is an installed version of python.

## Installation

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

Most of them are self-explanatory, however it should be noted that `max_hours` and `min_hours` only apply to **workdays**,
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

The following section will provide some useful examples for setting a `conf.py` file.

If you wish to only generate hours from Mon - Fri with a meeting on every Mon that goes for 2 hours, then you can use

```
# Black lists Sat and Sun
black_days = [5, 6]
# Every Mon will have at least 2 hours
event_days = {"0": 2.0}
```

Rounding and thresholding your hours can be achieved setting

```
# Will make sure all hours are >=30 minutes
hours_theshold = 0.5
# Will round all hours so that the minutes are multiple of 10
round_hours_by = 6
```

note that `hours_threshold` should be in between `[0, 1]` (it can in theory be bigger). If the value is `>1` it can cause issues with the generation process.
The rounding makes sure that all hours displayed in the xlsx file have a minute count of `n * 60 / round_hours_by`. Note that this can cause a deviation on your
total hours, so always make sure to check the output and the xlsx file. Also note, because of float inprecision, the rounding can be off by a minute.

Generating hours from a certain date to another certain date (as opposed to generting hours for the whole year), can be achieved by setting

```
year = 2022
start_date = datetime.date(year, 3, 15)
end_date = datetime.date(year, 8, 31)
```

which in this case, will generate hours from the 15th March to the 31th August. Leap years are being accounted for.

You can also create the hours completely manually by setting

```
# Black list all days
black_days = [0, 1, 2, 3, 4, 5, 6]
# Use the event days to manually set all hours
event_days = {"0": 2.0, "1": 3.0, "2": 5.5, "6": 2.0}
```

which will set **only** the event days and not generate any other hours (note that the program will still try to clip the hour values in between
`min_hours` and `max_hours`, and also try to increase/decrease the hours to your monthly hours).
