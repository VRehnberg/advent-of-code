from collections import Counter, namedtuple


class Card(int):
    def __new__(cls, label: str):
        if label.isdigit():
            value = int(label)
        else:
            value = {
                "T": 10,
                "J": 0,
                "Q": 12,
                "K": 13,
                "A": 15,
            }[label]
        return super().__new__(cls, value)

    def __repr__(self):
        if self > 9:
            return {
                10: "T",
                0:  "J",
                12: "Q",
                13: "K",
                15: "A",
            }[self]
        else:
            return super().__repr__()


class Hand():
    def __init__(self, hand: str):
        assert len(hand) == 5
        self.cards = tuple(Card(label) for label in hand)

    def __repr__(self):
        cards_str = "".join(map(repr, self.cards))
        return f"{self.__class__.__name__}({cards_str})"

    @property
    def strength(self):
        counter = Counter(self.cards)
        assert counter.total() == 5
        n_jokers = counter[Card("J")]
        most_common = counter.most_common()
        if n_jokers > 0 and n_jokers != 5:
            if Card("J") == most_common[0][0]:
                counter[most_common[1][0]] += n_jokers
            else:
                counter[most_common[0][0]] += n_jokers
            del counter[Card("J")]
        cards, counts = zip(*counter.most_common())
        assert sum(counts) == 5
        hand_type_strength = sum(4 ** c for c in counts)
        return (hand_type_strength, *self.cards)


Play = namedtuple("Play", ["hand", "bid"])


with open("7.in") as f:
    plays: list[Play] = []
    for line in f:
        hand, bid = line.split()
        plays.append(Play(hand=Hand(hand), bid=int(bid)))

# Sum rank * bid
plays.sort(key=lambda play: play.hand.strength)
assert len(set(repr(play.hand) for play in plays)) == len(plays)
print(*enumerate(plays), sep="\n")
print(sum(
    play.bid * (i + 1)
    for i, play in enumerate(plays)
))
