from collections import Counter
from enum import IntEnum

class CardValue:
	low_card = list(map(str, range(2, 10)))
	figures = ["T", "J", "Q", "K", "A"]
	values = low_card + figures
	values_order= {r: v for r, v in zip(low_card + figures, range(len(values)))}

	def __init__(self, card_value: str):
		self.value = card_value
		assert self.value in CardValue.values, f"Card value should be one of {CardValue.values}"

	def __gt__(self, other) -> bool:
		return CardValue.values_order[self.value] > CardValue.values_order[other.value]

	def __eq__(self, other) -> bool:
		return CardValue.values_order[self.value] == CardValue.values_order[other.value]

	def __sub__(self, other) -> int:
		return CardValue.values_order[self.value] - CardValue.values_order[other.value]

class Card(CardValue):
	def __init__(self, card: str):
		super().__init__(card[0])
		self.suit = card[1]

	def __repr__(self) -> str:
		return self.value + self.suit

class Rank(IntEnum):
	highest_card = 0
	one_pair = 1
	two_pairs = 2
	three_kind = 3
	straight = 4
	flush = 5
	full_house = 6
	four_kind = 7
	straight_flush = 8
	royal_flush = 9

class Hand:
	def __init__(self, list_of_cards: list[str]):
		self.hand = sorted([Card(c) for c in list_of_cards], reverse=True)
		print(self.hand)

	@property
	def _value_counter(self) -> Counter:
		return Counter([c.value for c in self.hand])

	def sort_value_counter(self) -> bool:
		sort_function = lambda x: (self._value_counter.get(x), CardValue.values_order[x])
		return sorted(self._value_counter, key=sort_function, reverse=True)

	def is_one_pair(self) -> bool:
		return max(self._value_counter.values()) == 2

	def is_two_pairs(self) -> bool:
		return sorted(self._value_counter.values()) == [1, 2, 2]

	def is_three_kind(self) -> bool:
		return max(self._value_counter.values()) == 3

	def is_straight(self) -> bool:
		no_pair = max(self._value_counter.values()) == 1
		range_card = max(self.hand) - min(self.hand)
		return no_pair and range_card == 4
	
	def is_flush(self) -> bool:
		return len(set(c.suit for c in self.hand)) == 1

	def is_full_house(self) -> bool:
		return set(self._value_counter.values()) == set([3, 2])

	def is_four_kind(self) -> bool:
		return max(self._value_counter.values()) == 4

	def is_straight_flush(self) -> bool:
		return self.is_flush() and self.is_straight()

	def is_royal_flush(self) -> bool:
		right_ranks = set(c.value for c in self.hand) == set(Card.figures)
		return self.is_flush() and right_ranks

	@property
	def rank(self) -> Rank:
		if self.is_royal_flush():
			rank = Rank.royal_flush
		elif self.is_straight_flush():
			rank = Rank.straight_flush
		elif self.is_four_kind():
			rank = Rank.four_kind
		elif self.is_full_house():
			rank = Rank.full_house
		elif self.is_flush():
			rank = Rank.flush
		elif self.is_straight():
			rank = Rank.straight
		elif self.is_three_kind():
			rank = Rank.three_kind
		elif self.is_two_pairs():
			rank = Rank.two_pairs
		elif self.is_one_pair():
			rank = Rank.one_pair
		else:
			rank = Rank.highest_card

		return rank

	def __gt__(self, other) -> bool:
		if self.rank == other.rank:
			card_order = self.sort_value_counter()
			other_card_order = other.sort_value_counter()
			i = 0
			while CardValue(card_order[i]) == CardValue(other_card_order[i]):
				i += 1
			return CardValue(card_order[i]) > CardValue(other_card_order[i])
		else:
			return self.rank > other.rank


print_threshold = 2
def p1_wins(hand_pairs: str) -> str:
	hand_pairs = hand_pairs.split()
	p1 = Hand(hand_pairs[:5])
	p2 = Hand(hand_pairs[5:])
	if p1.rank > print_threshold and p2.rank > print_threshold:
		print(p1.rank, p2.rank, (p1 > p2)*"P1" + (p1 < p2)*"P2" + "\n")
	return p1 > p2


Hands = [
	"5H 5C 6S 7S KD 2C 3S 8S 8D TD",
	"5D 8C 9S JS AC 2C 5C 7D 8S QH",
	"2D 9C AS AH AC 3D 6D 7D TD QD",
	"4D 6S 9H QH QC 3D 6D 7H QD QS",
	"2H 2D 4C 4D 4S 3C 3D 3S 9S 9D",
	"2H 3D 4C 5D 6D 2S 3S 4S 5S 6S",

]

assert ([p1_wins(h) for h in Hands]) == [False, True, False, True, True, False]

with open('p054_poker.txt') as f: lines = f.readlines()

print(sum([p1_wins(h) for h in lines]))