written_digits = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

with open("1.in") as f:
    calibration_sum = 0
    for line in f:
        # Get digits in string
        digits = ""
        for i, c in enumerate(line):
            # String representations of digits
            if c.isdigit():
                digits += c

            # Look for written digit starting from this point in the line
            for digit, written_digit in enumerate(written_digits):
                if line[i:].startswith(written_digit):
                    digits += f"{digit}"

        # Create calibration value and then add to sum
        calibration_value = int(digits[0] + digits[-1])
        assert calibration_value > 9 and calibration_value % 10 != 0
        calibration_sum += calibration_value

print(calibration_sum)
