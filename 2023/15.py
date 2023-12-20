def get_hash(step: str):
    hashval = 0
    for c in step:
        hashval += ord(c)
        hashval = (hashval * 17) % 256
    return hashval


with open("15.in") as f:
    line = next(f)

steps = line.strip().split(",")
print(sum(get_hash(step) for step in steps))
