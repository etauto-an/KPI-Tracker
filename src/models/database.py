# src/models/database.py

import sqlite3


class Database:
    """
    Handles database connection, table setup, and query execution.
    Manages a SQLite database for storing sales reps, metrics, and user roles.
    """

    def __init__(self, db_name="kpi_tracker_v2.db"):
        """
        Initializes the database connection and sets up tables.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        # Establish a connection to the SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create tables when the database is initialized
        self.setup_tables()

    def setup_tables(self):
        """
        Creates necessary tables if they do not already exist, including:
        - sales_rep_data: Stores daily metrics for each sales rep.
        - users: Stores user information, including roles for role-based access.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_rep_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rep_id TEXT,          -- References the user ID of the sales rep
                date TEXT,            -- Date of the metric entry
                scheduled_calls INTEGER,
                live_calls INTEGER,
                offers INTEGER,
                closed INTEGER,
                cash_collected REAL,
                contract_value REAL,
                FOREIGN KEY (rep_id) REFERENCES users (id)
            )
            """
        )

        # Table for users remains unchanged
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,          -- User ID, e.g., EMP001
                pin TEXT,                     -- Hashed PIN for security
                name TEXT,                    -- Name of the user
                role TEXT CHECK(role IN ('sales_rep', 'manager'))
                                              -- Role-based access restriction
            )
            """
        )

        self.conn.commit()

    def execute_query(self, query, params=()):
        """
        Executes a given SQL query with parameters and commits changes.

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters to use in the SQL query.
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """
        Fetches all results for a given SQL query.

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters to use in the SQL query.

        Returns:
            list: List of all results fetched from the database.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
