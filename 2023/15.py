from collections import defaultdict


def get_hash(step: str):
    hashval = 0
    for c in step:
        hashval += ord(c)
        hashval = (hashval * 17) % 256
    return hashval


with open("15.in") as f:
    line = next(f)

steps = line.strip().split(",")
#print(sum(get_hash(step) for step in steps))

# Initialization sequence
hashmap = defaultdict(dict)
for step in steps:
    label, instruction = step.split("=") if "=" in step else step.split("-")
    box = hashmap[get_hash(label)]
    if instruction:
        focal_length = int(instruction)
        hashmap[get_hash(label)][label] = focal_length
    elif label in box:
        del box[label]

#print(hashmap)

# Get focusing power
power_sum = 0
for i_box, lenses in hashmap.items():
    for i_lense, (label, focus_length) in enumerate(lenses.items()):
        focusing_power = (i_box + 1) * (i_lense + 1) * focus_length
        #print(label, focusing_power, i_box, i_lense, focus_length)
        power_sum += focusing_power
print(power_sum)




