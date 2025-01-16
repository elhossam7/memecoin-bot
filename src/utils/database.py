import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        """Initialize the database connection."""
        self.connection = self.create_connection(db_file)

    def create_connection(self, db_file):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        """Execute a single query."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(e)

    def fetch_all(self, query):
        """Fetch all results from a query."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def fetch_one(self, query):
        """Fetch a single result from a query."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()