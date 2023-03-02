import time
import random
import datetime

import numpy as np
from openpyxl.reader.excel import load_workbook

import generate_hours
import generate_xlsx


def main():
    generate_hours.main()
    generate_xlsx.main()


if __name__ == "__main__":
    main()

