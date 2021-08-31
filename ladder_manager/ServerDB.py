import sqlite3

from .constants import server_db_name

class ServerDB:
    """Database that stores information on admin accounts and preferences for ALL servers.
    
    Since this database covers all servers, the name of the file is fixed."""

    def __init__(self, name = server_db_name) -> None:
        assert name.endswith(".db")

        self.name = name

        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", ("users",))
        if self.cur.fetchone() is None:
            # run setup, since this is first time loading database for this ladder
            self.cur.execute(f"""CREATE TABLE users
                            (guild integer, id integer)""")
            self.cur.execute(f"""CREATE TABLE preferences
                            (guild integer, options text)""")

        self.con.commit()

    
    def add_admin(self, admin: int, guild: int) -> None:
        """Adds an admin to the database"""
        assert type(admin) is int
        assert type(guild) is int

        self.cur.execute("INSERT INTO users VALUES (?, ?)", (guild, admin))
        self.con.commit()


    def is_admin(self, guild: int, user: int) -> bool:
        """Checks if user is admin of guild."""
        self.cur.execute("SELECT * FROM users WHERE guild=? AND id=?", (guild, user))
        return self.cur.fetchone() is not None

    
    def is_guild_registered(self, guild: int) -> bool:
        """Checks if the guild has any admins (of this ladder bot)."""
        self.cur.execute("SELECT * FROM preferences WHERE guild=?", (guild,))
        return self.cur.fetchone() is not None