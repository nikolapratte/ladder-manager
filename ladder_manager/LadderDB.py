import sqlite3
from typing import Tuple

from .rating_calculators import calculate_ratings

class LadderDB:
    players_table = "players"
    starting_rating = 1200

    """Database for the ladder. Stores player information."""
    def __init__(self, ladder_name: str) -> None:
        """Sets up a new ladder database, using the provided filename.
        
        If the database already exists, uses that file."""
        assert ladder_name.endswith(".db"), f"Ladder names must end in .db, was provided {ladder_name}."

        self.name = ladder_name

        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
        
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (LadderDB.players_table,))
        if self.cur.fetchone() is None:
            # run setup, since this is first time loading database for this ladder
            self.cur.execute(f"""CREATE TABLE {LadderDB.players_table}
                            (id integer, rating integer)""")

        self.con.commit()
        # TODO can add history table later... and player statistics

    
    def _player_exists(self, player: int) -> bool:
        self.cur.execute("SELECT rating FROM players WHERE id=?", (player,))
        return self.cur.fetchone() is not None

    
    def _create_player(self, player: int) -> None:
        """Creates a player account"""
        self.cur.execute(f"INSERT INTO players VALUES (?, {LadderDB.starting_rating})", (player,))

    
    def _prepare_player(self, player: int) -> None:
        """After calling this, programmer can assume the player will exist in database.
        
        If the player does not exist, make an account for them."""
        if not self._player_exists(player):
            self._create_player(player)

    
    def _get_player_rating(self, player: int) -> int:
        """Retrieves the following player rating from the given ladder.
        
        Assumes that the player exists."""
        self.cur.execute("SELECT rating FROM players WHERE id=?", (player,))
        val = self.cur.fetchone()

        if val is None:
            raise ValueError("Received a player id for a player that does not exist.")

        return val[0]


    def process_match(self, ladder_name: str, player1: int, player2: int, matches: str) -> Tuple[int, int]:
        """Processes a match in the given ladder database with the given information.

        [player1] and [player2] should be the ids of the players, and [matches] should be
        a string of 1s for wins or 0s for losses from player1's perspective.
        
        Return: Tuple[player1_final_mmr, player2_final_mmr]"""
        self._prepare_player(player1)
        self._prepare_player(player2)

        p1starting_mmr = self._get_player_rating(player1)
        p2starting_mmr = self._get_player_rating(player2)

        p1final_mmr, p2final_mmr = calculate_ratings(p1starting_mmr, p2starting_mmr, matches)

        for player, rating in [(player1, p1final_mmr), (player2, p2final_mmr)]:
            self.cur.execute("UPDATE players SET rating = ? WHERE id = ?", (rating, player))
        self.con.commit()

        return p1final_mmr, p2final_mmr


if __name__ == "__main__":
    db = LadderDB("test_db.db")