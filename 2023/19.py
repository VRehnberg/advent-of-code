
with open("19.in") as f:

    # Workflows
    workflows = dict()
    for line in f:
        line = line.strip()
        if not line:
            break
        label, rules = line.split("{")
        workflows[label] = rules[:-1].split(",")

    # Parts
    parts = []
    for line in f:
        part = {}
        for attribute in line.strip()[1:-1].split(","):
            key, val = attribute.split("=")
            part[key] = int(val)
        parts.append(part)

#print(*workflows.items(), sep="\n")
#print(*parts, sep="\n")
def check_rule(part, diff):
    if ">" in diff:
        attr, val = diff.split(">")
        return part[attr] > int(val)
    elif "<" in diff:
        attr, val = diff.split("<")
        return part[attr] < int(val)
    else:
        raise RuntimeError

accepted = []
for part in parts:
    workflow = "in"
    while len(workflow) > 1:
        for rule in workflows[workflow]:
            if ":" not in rule:
                workflow = rule
                break
            diff, dest = rule.split(":")
            if check_rule(part, diff):
                workflow = dest
                break
    if workflow == "A":
        accepted.append(part)

print(sum(sum(p.values()) for p in accepted))
