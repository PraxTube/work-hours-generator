import sys
import random
import numpy as np


def random_hours(days, hours):
    hours_left = hours
    result = []
    for i in range(days-1):
        h = random.randint(0, min(4, hours_left - (days-i-1)))
        result.append(h)
        hours_left -= h
    result.append(hours_left)
    return result


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


def random_hours_dirichlet(days, hours, mi, ma):
    alphas = np.ones(days)
    weights = np.random.dirichlet(alphas)
    unbound =  [int(round(w * hours)) for w in weights]
    result = [min(ma, max(mi, x)) for x in unbound]

    if sum(result) < hours:
        increase_hours(result, hours, mi, ma)
    elif sum(result) > hours:
        decrease_hours(result, hours, mi, ma)

    return result


print(random_hours(int(sys.argv[1]), int(sys.argv[2])))
print(random_hours_dirichlet(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
