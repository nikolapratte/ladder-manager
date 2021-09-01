import os

import pytest

from ..ladder_manager.constants import test_db_filename
from ..ladder_manager.ServerDB import ServerDB

@pytest.fixture
def test_db():
    db = ServerDB(test_db_filename)

    yield db

    # cleanup generated file

    db.con.close()
    os.remove(test_db_filename)


def test_admin_check(test_db: ServerDB):
    assert test_db.is_admin(1, 1) is False

def test_admin_add(test_db: ServerDB):
    test_db.add_admin(1, 1)
    
    assert test_db.is_admin(1, 1) is True

def test_admin_add2(test_db: ServerDB):
    test_db.add_admin(1, 1)
    
    assert test_db.is_admin(1, 2) is False

def test_admin_add3(test_db: ServerDB):
    test_db.add_admin(1, 1)
    
    assert test_db.is_admin(2, 1) is False

def test_admin_guild_registered_false(test_db: ServerDB):
    test_db.add_admin(1, 1)
    
    assert test_db.is_guild_registered(2) is False

def test_admin_guild_registered_true(test_db: ServerDB):
    test_db.add_admin(1, 1)
    
    assert test_db.is_guild_registered(1) is True

def test_get_admin(test_db: ServerDB):
    test_db.add_admin(1, 1)
    test_db.add_admin(2, 2)
    test_db.add_admin(1, 2)
    
    assert test_db.get_admins(1) == (1, 2)


def test_get_admin_none(test_db: ServerDB):
    test_db.add_admin(1, 1)
    test_db.add_admin(2, 2)
    test_db.add_admin(1, 2)
    
    assert test_db.get_admins(3) == tuple()