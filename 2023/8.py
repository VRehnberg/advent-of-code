import re
from itertools import cycle


re_nodes = re.compile(r"^([A-Z]+) = [(]([A-Z]+), ([A-Z]+)[)]$")


with open("8.in") as f:
    instructions = next(f).strip()
    assert next(f).strip() == ""

    nodes: dict[str, tuple[str, str]] = {}
    for line in f:
        match = re_nodes.match(line.strip())
        nodes[match.group(1)] = (match.group(2), match.group(3))


instruct2index = {
    "L": 0,
    "R": 1,
}
location = "AAA"
for i_step, instruct in enumerate(cycle(instructions)):
    if location == "ZZZ":
        break
    location = nodes[location][instruct2index[instruct]]

print(i_step)
