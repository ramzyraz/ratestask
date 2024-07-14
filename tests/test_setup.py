import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime, timedelta
from app.config import Config

def connect_database():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def create_test_database(db_name):
    conn = connect_database()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()

def setup_test_data(conn):
    with conn.cursor() as cur:
        # Drop tables if they exist
        cur.execute("""
            DROP TABLE IF EXISTS prices;
            DROP TABLE IF EXISTS ports;
            DROP TABLE IF EXISTS regions;
        """)

        # Create tables
        cur.execute("""
            CREATE TABLE regions (
                slug TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                parent_slug TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE ports (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                parent_slug TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE prices (
                orig_code TEXT NOT NULL,
                dest_code TEXT NOT NULL,
                day DATE NOT NULL,
                price INTEGER NOT NULL
            )
        """)

        # Adding test data for regions
        cur.execute("""
            INSERT INTO regions (slug, name, parent_slug) VALUES 
            ('northern_europe', 'Northern Europe', NULL),
            ('north_europe_main', 'North Europe Main', 'northern_europe'),
            ('china_main', 'China Main', NULL)
        """)

        # Adding test data for ports
        cur.execute("""
            INSERT INTO ports (code, name, parent_slug) VALUES 
            ('CNSGH', 'Shanghai', 'china_main'), 
            ('NLRTM', 'Rotterdam', 'north_europe_main')
        """)

        # Adding test data for prices
        start_date = datetime(2023, 1, 1)
        for i in range(10):
            day = start_date + timedelta(days=i)
            for j in range(3):
                cur.execute("INSERT INTO prices (orig_code, dest_code, day, price) VALUES (%s, %s, %s, %s)",
                            ('CNSGH', 'NLRTM', day, 1000 + i*10 + j))

    conn.commit()
