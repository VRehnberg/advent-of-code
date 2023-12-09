import numpy as np


with open("9.in") as f:
    series = [
        np.array(line.strip().split(), dtype=int)
        for line in f
    ]

# Task 1
next_val_sum = 0
for serie in series:
    diffs = np.diff(serie)
    increments = [diffs[-1]]
    while np.count_nonzero(diffs) != 0:
        diffs = np.diff(diffs)
        increments.append(diffs[-1])

    print(increments)
    next_val = serie[-1] + sum(increments)
    next_val_sum += next_val
    print(next_val)

print(next_val_sum)
