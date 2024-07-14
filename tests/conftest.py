import pytest
from app import create_app
from app.config import Config
from .test_setup import connect_database, create_test_database, setup_test_data

@pytest.fixture(scope='session')
def app():
    test_db_name = "test_" + Config.DB_NAME
    create_test_database(test_db_name)

    Config.DB_NAME = test_db_name
    
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='function')
def client(app):
    # Creates a test client and allows you to make requests to your app without actually running the server.
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def db():
    conn = connect_database()
    setup_test_data(conn)    
    yield conn
    conn.close()
