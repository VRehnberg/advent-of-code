from collections import defaultdict


with open("2.in") as f:
    added_ids = 0
    sum_of_powers = 0
    for line in f:
        # Get ID of game
        assert line.startswith("Game ")
        id_part, game_part = line.split(":")
        assert id_part.startswith("Game ")
        game_id = int(id_part[5:])

        # Aggregate per color
        draws = defaultdict(list)
        for sub_game in game_part.strip().split(";"):
            for draw in sub_game.split(","):
                count, color = draw.strip().split()
                draws[color].append(int(count))

        ## Check if hypothetical count was possible
        ##print(line)
        ##print(draws)
        #if (
        #    max(draws["red"]) <= 12
        #    and max(draws["green"]) <= 13
        #    and max(draws["blue"]) <= 14
        #):
        #    added_ids += game_id
        #    #print(game_id, "possible")

        # Calculate power
        power = max(draws["red"]) * max(draws["green"]) * max(draws["blue"])
        #print(game_id, power)
        sum_of_powers += power

#print(added_ids)
print(sum_of_powers)
