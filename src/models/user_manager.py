# src/models/user_manager.py

from .database import Database


class UserManager:
    """
    Manages user-related data and operations, including adding and retrieving users.
    Handles role-based access by managing user roles (e.g., 'sales_rep' and 'manager').
    """

    def __init__(self, db: Database):
        """
        Initializes UserManager with a database instance.

        Args:
            db (Database): Instance of the Database class for data operations.
        """
        self.db = db

    def add_user(self, user_id, pin, name, role="sales_rep"):
        """
        Adds a new user to the database.

        Args:
            user_id (str): Unique identifier for the user.
            pin (str): Hashed PIN for user authentication.
            name (str): Name of the user.
            role (str): Role of the user, either 'sales_rep' or 'manager'.
        """
        self.db.execute_query(
            """
            INSERT INTO users (id, pin, name, role)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, pin, name, role),
        )

    def get_user(self, user_id):
        """
        Retrieves user information based on user ID.

        Args:
            user_id (str): The user ID to retrieve.

        Returns:
            dict: User information including id, pin, name, and role if the user
                  exists.
                  None if the user is not found.
        """
        result = self.db.fetch_all(
            """
            SELECT id, pin, name, role FROM users WHERE id = ?
            """,
            (user_id,),
        )
        if result:
            # Return as a dictionary to allow access by keys like "pin"
            return {
                "id": result[0][0],
                "pin": result[0][1],
                "name": result[0][2],
                "role": result[0][3],
            }
        return None

    def get_all_users(self):
        """
        Retrieves all users in the system, mainly for KPI calculations.

        Returns:
            list: List of dictionaries with user information for all users.
        """
        results = self.db.fetch_all("SELECT id, name, role FROM users")
        return [
            {"id": row[0], "name": row[1], "role": row[2]} for row in results
        ]

    def validate_user_id(self, user_id):
        """
        Checks if a user ID already exists in the database.

        Args:
            user_id (str): The user ID to validate.

        Returns:
            bool: True if the user ID does not exist, False otherwise.
        """
        query = "SELECT COUNT(*) FROM users WHERE id = ?"
        try:
            result = self.db.fetch_all(query, (user_id,))
            # If the result is empty or returns a count of 0, the user ID is valid
            return result and result[0][0] == 0
        except Exception as e:
            print(f"Error validating user ID: {e}")
            return False
