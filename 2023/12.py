import re
from itertools import pairwise, product

from tqdm import tqdm


re_broken_groups: dict[int, re.Pattern] = {
    i: re.compile(r"(?:^|[.?])(?=([#?]{" + f"{i}" + "}))")
    for i in range(1, 20)
}
re_group_end = re.compile("^(?:[.?]|$)")

with open("12.in") as f:
    n_arrangements = 0
    for line in tqdm(f.readlines()):
        pattern, counts = line.strip().split()
        pattern = pattern.strip()
        counts = list(map(int, counts.split(",")))

        #print(counts, re_broken_groups[counts[0]])
        list_possible_groups: list[list[range]] = []
        prev_min_stop = -1
        for count in counts:
            possible_groups: list[range] = []
            min_stop = 0
            for match in re_broken_groups[count].finditer(pattern):
                start, stop = match.regs[1]
                #print(start, stop, pattern[start:stop], pattern[stop] if len(pattern) > stop else "", re_group_end.match(pattern[stop:]), pattern[stop:])
                if start > prev_min_stop and re_group_end.match(pattern[stop:]):
                    possible_groups.append(range(start, stop))
                    min_stop = min(stop, min_stop)
            list_possible_groups.append(possible_groups)
            prev_min_stop = min_stop

        n_tmp = 0
        for groups in product(*list_possible_groups):
            for group0, group1 in pairwise(groups):
                if group0.stop >= group1.start:
                    break
            if group0.stop < group1.start:
                n_arrangements += 1
                n_tmp += 1

print(n_arrangements)
