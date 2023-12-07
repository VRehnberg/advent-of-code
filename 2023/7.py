from collections import Counter, namedtuple


class Card(int):
    def __new__(cls, label: str):
        if label.isdigit():
            value = int(label)
        else:
            value = {
                "T": 10,
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 15,
            }[label]
        return super().__new__(cls, value)

    def __repr__(self):
        if self > 9:
            return {
                10: "T",
                11: "J",
                12: "Q",
                13: "K",
                15: "A",
            }[self]
        else:
            return super().__repr__()


class Hand():
    def __init__(self, hand: str):
        assert len(hand) == 5
        self.counter = Counter((Card(label) for label in hand))
        assert self.counter.total() == 5

    def __repr__(self):
        hand = "".join(
            repr(card) for count, card in self.score for _ in range(count)
        )
        return f"{self.__class__.__name__}({hand})"

    @property
    def score(self):
        return tuple(
            sorted(
                ((count, card) for card, count in self.counter.items()),
                reverse=True,
            )
        )


Play = namedtuple("Play", ["hand", "bid"])


with open("7.in") as f:
    plays: list[Play] = []
    for line in f:
        hand, bid = line.split()
        plays.append(Play(hand=Hand(hand), bid=int(bid)))

# Sum rank * bid
plays.sort(key=lambda play: play.hand.score)
assert len(set(repr(play.hand) for play in plays)) == len(plays)
print(*enumerate(plays), sep="\n")
print(sum(
    play.bid * (i + 1)
    for i, play in enumerate(plays)
))
