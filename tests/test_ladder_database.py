import os

import pytest

from ..ladder_manager.LadderDB import LadderDB

from ..ladder_manager.constants import test_db_filename

@pytest.fixture
def test_db():
    db = LadderDB()

    db.setup_ladder(test_db_filename)

    yield db

    # cleanup generated file
    os.remove(test_db_filename)


def test_database_file_exists_after_creation(test_db):
    assert os.path.exists(test_db_filename)

