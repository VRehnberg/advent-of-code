import numpy as np


def get_dish(file) -> np.array:
    return np.array([list(line.strip()) for line in file])

def get_weight(col):
    distance = len(col)
    weight = 0
    for i, c in enumerate(col):
        if c == ".":
            continue
        elif c == "#":
            distance = len(col) - (i + 1)
        elif c == "O":
            weight += distance
            distance -= 1
        else:
            RuntimeError
    #print(col, weight)
    return weight


with open("14.in") as f:
    dish = get_dish(f)

weight = sum(get_weight(col) for col in dish.T)
print(weight)
