"""Day 7: Camel Cards"""

import collections
import functools


_PART_ONE_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
_PART_TWO_ORDER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def replace_jokers(hand: str) -> str:
    """Replaces jokers in a hand with the cards that make the hand highest scoring."""
    counts = collections.Counter(hand)
    _ = counts.pop("J", None)
    ranked = sorted(
        counts.items(), key=lambda x: (x[1], _PART_TWO_ORDER.index(x[0])), reverse=True
    )
    if not ranked:
        return "AAAAA"
    return hand.replace("J", ranked[0][0])


def compare_hands(first: str, second: str, is_part_two: bool) -> int:
    """Calculates the winner of a hand. 1 = first wins, -1 = second wins, 0 = draw."""
    first_to_count = replace_jokers(first) if is_part_two else first
    second_to_count = replace_jokers(second) if is_part_two else second
    first_counts = sorted(collections.Counter(first_to_count).values(), reverse=True)
    second_counts = sorted(collections.Counter(second_to_count).values(), reverse=True)
    card_ranks = _PART_TWO_ORDER if is_part_two else _PART_ONE_ORDER

    # If the hands have the same counts, use the secondary comparison method.
    if first_counts == second_counts:
        for first_card, second_card in zip(first, second):
            if card_ranks.index(first_card) > card_ranks.index(second_card):
                return 1
            elif card_ranks.index(first_card) < card_ranks.index(second_card):
                return -1
        return 0

    # If both hands have the same maximum repeats of a card, then check the next most
    # repeated card to break the tie.
    if first_counts[0] == second_counts[0]:
        if first_counts[1] > second_counts[1]:
            return 1
        elif first_counts[1] < second_counts[1]:
            return -1

    # If the max number of repeats of a card is higher in either case, that hand wins.
    if first_counts[0] > second_counts[0]:
        return 1
    return -1


def parse_input(hands: str) -> dict[str, int]:
    """Parses some hands into a dictionary."""
    hand_to_bid = {}
    for hand_and_bid in hands.splitlines():
        hand, bid = hand_and_bid.split()
        hand_to_bid[hand] = int(bid)
    return hand_to_bid


def solve(hands: str, is_part_two: bool) -> int:
    """Gets the total winnings from a set of hands and corresponding bids."""
    hand_to_bid = parse_input(hands)
    sorted_hands = sorted(
        hand_to_bid.items(),
        key=functools.cmp_to_key(lambda x, y: compare_hands(x[0], y[0], is_part_two)),
        reverse=False,
    )
    return sum(i * b[1] for i, b in enumerate(sorted_hands, start=1))


def main():
    with open("input.txt", "r") as f:
        hands = f.read()

    print("Part 1: ", solve(hands, is_part_two=False))
    print("Part 2: ", solve(hands, is_part_two=True))


if __name__ == "__main__":
    main()
