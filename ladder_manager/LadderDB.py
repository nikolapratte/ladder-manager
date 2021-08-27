import sqlite3

class LadderDB:
    """Database for the ladder. Stores player information."""
    def __init__(self):
        pass

    def setup_ladder(self, ladder_name: str) -> None:
        """Sets up a new ladder database, using the provided filename."""
        assert ladder_name.endswith(".db"), f"Ladder names must end in .db, was provided {ladder_name}."

        con = sqlite3.connect(ladder_name)
        cur = con.cursor()

        cur.execute("""CREATE TABLE players
                        (id integer, rating integer, wins integer, losses integer)""")
                        
        con.commit()
        con.close()

        # TODO can add history table later...
