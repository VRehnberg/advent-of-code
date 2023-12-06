import numpy as np


with open("6.in") as f:
    times = tuple(map(int, next(f).split(":")[-1].strip().split()))
    record_distances = tuple(map(int, next(f).split(":")[-1].strip().split()))

    n_possible_wins = []
    for time, record_distance in zip(times, record_distances):
        speed = np.arange(0, time + 1)
        run_time = time - speed
        n_possible_wins.append(np.count_nonzero(run_time * speed > record_distance))

print(n_possible_wins)
print(np.prod(n_possible_wins))
