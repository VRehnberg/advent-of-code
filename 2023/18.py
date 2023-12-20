i, j = 0, 0
with open("18.in") as f:
    edges = {}
    for line in f:
        direction, dist, color = line.strip().split()
        dist = int(dist)

        for step in range(dist):
            #print(i, j, direction)
            if direction == "R":
                j += 1
            elif direction == "L":
                j -= 1
            elif direction == "U":
                i -= 1
            elif direction == "D":
                i += 1

            if i not in edges:
                edges[i] = (j, j + 1)
            else:
                edges[i] = (
                    min(j, edges[i][0]),
                    max(j + 1, edges[i][1]),
                )

volume = sum(r - l for l, r in edges.values())
#print(edges)
print(volume)
