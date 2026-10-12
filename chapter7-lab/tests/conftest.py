import pytest

from app import app, init_db


@pytest.fixture()
def client(tmp_path):
    app.config.update(TESTING=True, DB_PATH=str(tmp_path / "test.db"))
    init_db()
    with app.test_client() as c:
        yield c
