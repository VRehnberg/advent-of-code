from collections import defaultdict


with open("4.in") as f:

    score = 0
    scratch_card_counter = defaultdict(lambda: 0)
    for line in f:
        card_id, game = line.split(":")
        card_id = int(card_id[5:])
        scratch_card_counter[card_id] += 1

        winning_numbers, my_numbers = game.split("|")
        winning_numbers = set(map(int, winning_numbers.strip().split()))
        my_numbers = set(map(int, my_numbers.strip().split()))

        overlap = winning_numbers & my_numbers
        score += int(2 ** (len(overlap) - 1))

        for won_card_id in range(card_id + 1, card_id + len(overlap) + 1):
            # Add cards
            scratch_card_counter[won_card_id] += scratch_card_counter[card_id]

    for non_existent_card_id in range(card_id + 1, len(scratch_card_counter)):
        scratch_card_counter[non_existent_card_id] = 0

print(score)
print(sum(scratch_card_counter.values()))
