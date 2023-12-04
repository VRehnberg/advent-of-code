with open("4.in") as f:

    score = 0
    for line in f:
        card_id, game = line.split(":")
        card_id = int(card_id[5:])
        winning_numbers, my_numbers = game.split("|")
        winning_numbers = set(map(int, winning_numbers.strip().split()))
        my_numbers = set(map(int, my_numbers.strip().split()))

        overlap = winning_numbers & my_numbers
        score += int(2 ** (len(overlap) - 1))

print(score)
