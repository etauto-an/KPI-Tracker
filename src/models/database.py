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

        # Automatically set up tables during initialization
        self.setup_tables()

    def setup_tables(self):
        """
        Creates necessary tables if they do not already exist, including:
        - sales_rep_data: Stores daily metrics for each sales rep.
        - users: Stores user information, including roles for role-based access.
        """
        # Create the 'sales_rep_data' table for storing daily metrics
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_rep_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing unique ID
                rep_id TEXT,                           -- References the user ID of the sales rep
                date TEXT,                             -- Date of the metric entry
                scheduled_calls INTEGER,               -- Number of scheduled calls
                live_calls INTEGER,                    -- Number of live calls made
                offers INTEGER,                        -- Number of offers presented
                closed INTEGER,                        -- Number of deals closed
                cash_collected REAL,                   -- Amount of cash collected
                contract_value REAL,                   -- Total contract value of closed deals
                FOREIGN KEY (rep_id) REFERENCES users (id) -- Relationship with users table
            )
            """
        )

        # Create the 'users' table to store user credentials and roles
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,          -- User ID (unique), e.g., EMP001
                pin TEXT,                     -- Hashed PIN for security purposes
                name TEXT,                    -- Name of the user
                role TEXT CHECK(role IN ('sales_rep', 'manager')), -- Restrict roles to predefined types
                UNIQUE(id)                    -- Enforce unique User IDs
            )
            """
        )

        # Commit the changes to persist table structures in the database
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

    def insert_user(self, user_id, name, pin, role):
        """
        Inserts a new user into the 'users' table.

        Args:
            user_id (str): Unique identifier for the user (e.g., EMP001).
            name (str): Name of the user.
            pin (str): Hashed PIN for authentication.
            role (str): Role of the user (e.g., 'sales_rep', 'manager').

        Returns:
            dict: A dictionary containing the operation result:
                  - success (bool): True if the user is added successfully, False otherwise.
                  - message (str): Success or error message.
        """
        try:
            # Attempt to insert a new user into the database
            self.execute_query(
                """
                INSERT INTO users (id, name, pin, role)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, name, pin, role),
            )
            return {"success": True, "message": "User added successfully."}
        except sqlite3.IntegrityError as e:
            # Handle duplicate User ID or other integrity issues
            if "UNIQUE constraint failed" in str(e):
                return {"success": False, "message": "User ID already exists."}
            else:
                return {"success": False, "message": str(e)}
