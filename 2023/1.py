import re


with open("1.in") as f:
    calibration_sum = 0
    re_digit = re.compile("\D+", flags=re.ASCII)
    for line in f:
        # Remove non digit characters
        digits = re_digit.sub("", line)

        # Create calibration value and then add to sum
        calibration_value = int(digits[0] + digits[-1])
        calibration_sum += calibration_value

print(calibration_sum)
