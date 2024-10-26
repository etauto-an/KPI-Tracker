# database.py
import sqlite3


class Database:
    """
    Handles database connection, table setup, and query execution.
    Manages a SQLite database for storing sales reps and metrics.
    """

    def __init__(self, db_name="kpi_tracker_v2.db"):
        # Initialize the database connection
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Create tables when the database is initialized
        self.setup_tables()

    def setup_tables(self):
        """
        Creates tables if they do not already exist.
        Tables: sales_rep, sales_rep_data
        """
        # Table for sales reps
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_rep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """
        )

        # Table for daily metrics
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_rep_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rep_id INTEGER,
                date TEXT,
                scheduled_calls INTEGER,
                live_calls INTEGER,
                offers INTEGER,
                closed INTEGER,
                cash_collected REAL,
                contract_value REAL,
                FOREIGN KEY (rep_id) REFERENCES sales_rep (id)
            )
        """
        )
        # Commit changes to the database
        self.conn.commit()

    def execute_query(self, query, params=()):
        """
        Executes a given SQL query with parameters and commits changes.
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """
        Executes a SELECT query with parameters and fetches all results.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
