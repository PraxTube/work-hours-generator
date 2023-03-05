# Work Hours Generator

Generates random work hours in a given time frame and outputs the result in a xlsx file.

## Prerequisites

All that is required to use this repo is an installed version of python (`version>=3.8<=3.10` works, the rest hasn't been tested).

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

The **Advanced** settings:

```
black_days - list, Mark specific days as non workdays, i.e. [5, 6] will generate no hours for Sat, Sun
event_days - dict, Mark specific days as eventdays, great for simulating meetings, i.e. "0": 2.0 will make sure at least 2 hours on every Mon
hours_threshold - float in [0, 1], Any workdays below this value will be set to 0
round_hours_by - int, Rounds all work hours by this value: round(hours / round_hours_by) * round_hours_by, i.e. 4 will make sure minutes % 15 = 0
```

For more info on these settings see the `conf.py` file and the examples below.

## Examples

The following section will provide some usefull examples for setting a `conf.py` file.

