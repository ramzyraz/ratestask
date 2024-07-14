import psycopg2
from dotenv import load_dotenv
from flask import Flask, g
from .config import Config
from .routes import routes

load_dotenv()
 
def connect_db(logger):
    try:
        connection = psycopg2.connect(
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        return connection
    except psycopg2.OperationalError as e:
        logger.error(f"OperationalError: {e}")
    except psycopg2.InterfaceError as e:
        logger.error(f"InterfaceError: {e}")
    except psycopg2.DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")

    return None

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Establishes the database connection before each request
    @app.before_request
    def before_request():
        g.db = connect_db(app.logger)

    # Closes the database connection after each request
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    # Blueprint registeration
    app.register_blueprint(routes)
    return app