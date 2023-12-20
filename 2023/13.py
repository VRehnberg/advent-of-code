from typing import IO, Iterator

import numpy as np


def get_blocks(file: IO) -> Iterator[np.array]:
    block = []
    for line in file:
        if not line.strip():
            yield np.array(block, dtype=str)
            block = []
        else:
            block.append(list(line.strip()))
    yield np.array(block, dtype=str)


def check_horizontal_mirror(block):
    height, width = block.shape
    for i in range(height):
        mirror_line = i + 1
        mirror_height = min(mirror_line, height - mirror_line)
        sub_block = block[mirror_line - mirror_height : mirror_line + mirror_height, :]
        if sub_block.size and np.array_equal(sub_block, np.flip(sub_block, axis=0)):
            #print(sub_block)
            return mirror_line
    return 0

def main():
    with open("13.in") as f:
        count = 0
        for block in get_blocks(f):
            count += (
                (100 * check_horizontal_mirror(block))
                or check_horizontal_mirror(np.transpose(block))
            )
            print(count)
            #print(block)


if __name__ == "__main__":
    main()
