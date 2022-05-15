import pytest
import core
import db
@pytest.fixture()
def app():
    db.initialize_empty_database(db)
    db.populate_sample_data(db)
    app = core.app
    app.config.update({ "TESTING":True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()