from itertools import combinations

import numpy as np


np.set_printoptions(linewidth=140)


# Parse file
with open("11.in") as file:
    raw = np.array(
        [
            [s for s in line.strip()]
            for line in file
        ],
        dtype=str,
    )
print(raw)


# Expand
expansion_factor = 1000000
row_step = np.ones_like(raw, dtype=int)
for i in range(raw.shape[0]):
    if np.all(raw[i, :] == "."):
        row_step[i, :] *= expansion_factor
col_step = np.ones_like(raw, dtype=int)
for j in range(raw.shape[1]):
    if np.all(raw[:, j] == "."):
        col_step[:, j] *= expansion_factor

# Get pairwise distances
print(row_step, col_step)
galaxies = zip(*np.where(raw == "#"))
total_dist = 0
for (i0, j0), (i1, j1) in combinations(galaxies, 2):
    i_start = min(i0, i1)
    i_stop = max(i0, i1)
    j_start = min(j0, j1)
    j_stop = max(j0, j1)
    total_dist += (
        np.sum(row_step[i_start:i_stop, j_start])
        + np.sum(col_step[i_stop, j_start:j_stop])
    )
print("Sum of distances:", total_dist)
