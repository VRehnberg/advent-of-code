import numpy as np


with open("6.in") as f:
    time = int("".join(next(f).split(":")[-1].split()))
    record_distance = int("".join(next(f).split(":")[-1].split()))

speed = np.arange(0, time + 1)
run_time = time - speed
n_possible_wins = np.count_nonzero(run_time * speed > record_distance)

print(n_possible_wins)
