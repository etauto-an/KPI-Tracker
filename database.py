import sqlite3


class Database:
    """
    Handles database connection, table setup, and query execution.
    Manages a SQLite database for storing sales reps, metrics, and user roles.
    """

    def __init__(self, db_name="kpi_tracker_v2.db"):
        # Initialize the database connection
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Create tables when the database is initialized
        self.setup_tables()

    def setup_tables(self):
        """
        Creates tables if they do not already exist, including a users table with role-based access.
        """
        # Update the sales_rep table to use the id as the primary key (auto-incremented)
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_rep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- This will act as employee_id
                name TEXT
            )
            """
        )

        # Table for daily metrics remains unchanged
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

        # Table for users with roles for role-based access
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,       -- user ID, e.g., EMP001
                pin TEXT,                  -- hashed PIN for security
                name TEXT,
                role TEXT CHECK(role IN ('sales_rep', 'manager'))  -- restrict role to 'sales_rep' or 'manager'
            )
            """
        )

        self.conn.commit()

    def execute_query(self, query, params=()):
        """
        Executes a given SQL query with parameters and commits changes.
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """
        Fetches all rows for a given SQL query.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
