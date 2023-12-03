import re
from collections import deque
from itertools import chain


re_number = re.compile("\d+")
re_symbol = re.compile("[^0-9.]")


with open("3.in") as f:

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
