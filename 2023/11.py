from itertools import combinations

import numpy as np


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
space = raw
tmp = space
n_expanded = 0
for i in range(tmp.shape[0]):
    if np.all(tmp[i, :] == "."):
        space = np.insert(space, i + n_expanded, tmp[i, :], 0)
        n_expanded += 1
tmp = space
n_expanded = 0
for j in range(tmp.shape[1]):
    if np.all(tmp[:, j] == "."):
        space = np.insert(space, j + n_expanded, tmp[:, j], 1)
        n_expanded += 1
print(space)

# Get pairwise distances
galaxies = zip(*np.where(space == "#"))
distances = (
    abs(i0 - i1) + abs(j0 - j1)
    for (i0, j0), (i1, j1) in combinations(galaxies, 2)
)
print("Sum of distances:", sum(distances))
