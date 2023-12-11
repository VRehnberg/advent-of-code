import numpy as np


with open("9.in") as f:
    series = [
        np.array(line.strip().split(), dtype=int)
        for line in f
    ]

# Task 2
prev_val_sum = 0
for serie in series:
    #print("S", serie)
    diffs = np.diff(serie)
    #print("D", diffs)
    decrements = [diffs[0]]
    while np.count_nonzero(diffs) != 0:
        diffs = np.diff(diffs)
        decrements.append(diffs[0])
        #print("D", diffs)
    #print(decrements)

    prev_val = serie[0]
    meta_decrement = 0
    for i, decrement in enumerate(decrements[::-1]):
        meta_decrement = decrement - meta_decrement
        #print(i, meta_decrement)
    prev_val -= meta_decrement
    print(prev_val)
    prev_val_sum += prev_val

print(prev_val_sum)
