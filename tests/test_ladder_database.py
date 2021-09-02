import os
import time

import pytest

from ..ladder_manager.LadderDB import LadderDB
from ..ladder_manager.rating_calculators import base_rating_change, inequality_change_rate
from ..ladder_manager.constants import test_db_filename

@pytest.fixture
def test_db():
    db = LadderDB(test_db_filename)

    yield db

    # cleanup generated file

    db.con.close()
    os.remove(test_db_filename)


def test_database_file_exists_after_creation(test_db: LadderDB):
    assert os.path.exists(test_db_filename)


def test_database_doesnt_crash_if_exists():
    db = LadderDB(test_db_filename)
    del db

    db2 = LadderDB(test_db_filename)

    db2.con.close()
    os.remove(test_db_filename)


def testplayer_exists(test_db: LadderDB):
    assert test_db.player_exists(124) is False


def testplayer_exists_true(test_db: LadderDB):
    test_db.cur.execute("INSERT INTO players VALUES (42, 7000)")
    assert test_db.player_exists(42) is True


def test_player_create(test_db: LadderDB):
    test_db._create_player(2)
    assert test_db.player_exists(2) is True


def test_player_get_rating(test_db: LadderDB):
    test_db._create_player(3495)
    assert test_db.get_player_rating(3495) == LadderDB.starting_rating


def test_player_get_rating_exception_player_does_not_exist(test_db: LadderDB):
    with pytest.raises(ValueError):
        test_db.get_player_rating(432)


def test_process_match_simple(test_db: LadderDB):
    test_db._create_player(1)
    test_db._create_player(2)
    p1output, p2output = test_db.process_match(1, 2, "111")

    delta1 = base_rating_change - (0//inequality_change_rate)
    delta2 = base_rating_change - ((0 + delta1 * 2)//inequality_change_rate)
    delta3 = base_rating_change - ((0 + delta1 * 2 + delta2 * 2)//inequality_change_rate)
    delta = delta1 + delta2 + delta3

    assert p1output == 1200 + delta
    assert p2output == 1200 - delta
    
    assert test_db.get_player_rating(1) == 1200 + delta
    assert test_db.get_player_rating(2) == 1200 - delta


def test_process_match_simple_save():
    test_db = LadderDB(test_db_filename)

    test_db._create_player(1)
    test_db._create_player(2)
    p1output, p2output = test_db.process_match(1, 2, "111")

    delta1 = base_rating_change - (0//inequality_change_rate)
    delta2 = base_rating_change - ((0 + delta1 * 2)//inequality_change_rate)
    delta3 = base_rating_change - ((0 + delta1 * 2 + delta2 * 2)//inequality_change_rate)
    delta = delta1 + delta2 + delta3

    test_db.con.close()
    db2 = LadderDB(test_db_filename)
    
    assert db2.get_player_rating(1) == 1200 + delta
    assert db2.get_player_rating(2) == 1200 - delta

    db2.con.close()

    os.remove(test_db_filename)


def test_board(test_db: LadderDB):
    test_db._create_player(1)
    test_db._create_player(2)
    p1output, p2output = test_db.process_match(1, 2, "111")

    assert test_db.board() == [(1, p1output), (2, p2output)]


def test_board2(test_db: LadderDB):
    test_db._create_player(1)
    test_db._create_player(2)
    test_db._create_player(3)
    p1output, p2output = test_db.process_match(1, 2, "111")

    assert test_db.board() == [(1, p1output), (3, LadderDB.starting_rating), (2, p2output)]


def test_history(test_db: LadderDB):
    test_db._create_player(1)
    test_db._create_player(2)
    p1output, p2output = test_db.process_match(1, 2, "111")

    test_db.cur.execute("SELECT * FROM history")
    values = test_db.cur.fetchone()

    assert values == (1, 2, 1200, 1200, "111")


def test_update(test_db: LadderDB):
    test_db._create_player(1)
    test_db.update_player(1, 2000)

    assert test_db.get_player_rating(1) == 2000


def test_update_does_not_exist(test_db: LadderDB):
    test_db._create_player(1)
    test_db.update_player(2, 2000)

    assert test_db.get_player_rating(2) == 2000