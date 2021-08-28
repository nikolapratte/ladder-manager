from typing import Tuple


# constants

base_rating_change = 25
# for every [inequality_change_rate] difference, change [base_rating_change]
# by 1 (either add or subtract, depending on who wins)
inequality_change_rate = 20


def calculate_match(player1_mmr: int, player2_mmr: int, p1_won: bool) -> Tuple[int, int]:
    """Calculates mmr after one match."""

    # can refactor, left in this way to make it easier to imagine control flows
    if player1_mmr >= player2_mmr:
        diff = player1_mmr - player2_mmr
        expectation = diff//inequality_change_rate
        if p1_won:
            delta = max(base_rating_change - expectation, 1)
            player1_mmr += delta
            player2_mmr -= delta
        else:
            delta = min(base_rating_change + expectation, 2 * base_rating_change)
            player1_mmr -= delta
            player2_mmr += delta
    else:
        # if player2 is favored
        diff = player2_mmr - player1_mmr
        expectation = diff//inequality_change_rate
        if p1_won:
            delta = min(base_rating_change + expectation, 2 * base_rating_change)
            player1_mmr += delta
            player2_mmr -= delta
        else:
            delta = max(base_rating_change - expectation, 1)
            player1_mmr -= delta
            player2_mmr += delta

    return player1_mmr, player2_mmr


def calculate_ratings(player1_mmr: int, player2_mmr: int, matches: str) -> Tuple[int, int]:
    """Calculates the final ratings of p1 and p2 if they have the given mmrs at the start,
    and play the series of [matches], where 1s are wins and 0s are losses in p1's perspective."""

    for match in matches:
        assert match == "0" or match == "1", "Matches should only include 1s or 0s in a string."

        player1_mmr, player2_mmr = calculate_match(player1_mmr, player2_mmr, match == "1")
    
    return player1_mmr, player2_mmr


if __name__ == "__main__":
    calculate_match(1300, 1300, False)