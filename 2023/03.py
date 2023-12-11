import re
from collections import deque
from itertools import chain


re_number = re.compile("\d+")
re_symbol = re.compile("[^0-9.]")
re_gear = re.compile("[*]")


def task1(filename: str = "3.in"):
    with open(filename) as f:

        line_window = deque(maxlen=3)
        counter = 0
        while True:
            try:
                line_window.append(next(f).strip())
                if len(line_window) == 1:
                    continue
                number_line = line_window[-2]
            except StopIteration:
                line_window.popleft()
                if len(line_window) == 1:
                    break
                number_line = line_window[1]

            # Get relevant
            symbols = list(chain(*[
                re_symbol.finditer(l)
                for l in line_window
            ]))
            #print('--------------------------------')
            #print('\n'.join([l for l in line_window]))
            #print(*[s for s in symbols], sep="\n")
            numbers = re_number.finditer(number_line)

            # Count numbers
            for number in numbers:
                number_used = False
                for symbol in symbols:
                    #print(symbol)
                    assert symbol.start() + 1 == symbol.end()
                    if symbol.start() in range(number.start() - 1, number.end() + 1):
                        number_used = True
                        counter += int(number.group())
                        break
                #print(number, number_used)

    print(counter)


def task2(filename: str = "3.in"):
    with open(filename) as f:

        line_window = deque(maxlen=3)
        counter = 0
        while True:
            try:
                line_window.append(next(f).strip())
                if len(line_window) == 1:
                    continue
                gear_line = line_window[-2]
            except StopIteration:
                line_window.popleft()
                if len(line_window) == 1:
                    break
                gear_line = line_window[1]

            numbers = list(chain(*[
                re_number.finditer(l)
                for l in line_window
            ]))
            gears = re_gear.finditer(gear_line)

            # Count numbers
            for gear in gears:
                uses: list[int] = []
                for number in numbers:
                    if gear.start() in range(number.start() - 1, number.end() + 1):
                        uses.append(int(number.group()))

                if len(uses) == 2:
                    counter += uses[0] * uses[1]

    print(counter)


def main():
    filename = "3.in"
    task1(filename)
    task2(filename)


if __name__ == "__main__":
    main()
