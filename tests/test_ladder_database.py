import os
import time

import pytest

from ..ladder_manager.LadderDB import LadderDB

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



def test_player_exists(test_db: LadderDB):
    assert test_db._player_exists(124) is False


def test_player_exists_true(test_db: LadderDB):
    test_db.cur.execute("INSERT INTO players VALUES (42, 7000)")
    assert test_db._player_exists(42) is True


def test_player_create(test_db: LadderDB):
    test_db._create_player(2)
    assert test_db._player_exists(2) is True


def test_player_get_rating(test_db: LadderDB):
    test_db._create_player(3495)
    assert test_db._get_player_rating(3495) == LadderDB.starting_rating


def test_player_get_rating_exception_player_does_not_exist(test_db: LadderDB):
    with pytest.raises(ValueError):
        test_db._get_player_rating(432)