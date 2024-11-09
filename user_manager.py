# user_manager.py
import sqlite3
from database import Database


class UserManager:
    """
    Manages user-related operations, including adding users and retrieving user information.
    Supports role-based access control by managing user roles.
    """

    def __init__(self, db: Database):
        self.db = db  # Reference to the Database instance

    def add_user(self, user_id, pin, name, role):
        """
        Adds a new user to the database with a specified role.
        Allowed roles are 'sales_rep' and 'manager'.
        """
        try:
            self.db.execute_query(
                "INSERT INTO users (id, pin, name, role) VALUES (?, ?, ?, ?)",
                (user_id, pin, name, role),
            )
            print(
                f"User {name} added successfully with ID {user_id} and role {role}."
            )
        except sqlite3.IntegrityError:
            print("Error: A user with this ID already exists.")
        except Exception as e:
            print(f"Error: {e}")

    def get_user(self, user_id):
        """
        Retrieves user details by user ID, including the role.
        Returns a dictionary with user information if found, otherwise None.
        """
        result = self.db.fetch_all(
            "SELECT id, pin, name, role FROM users WHERE id = ?", (user_id,)
        )
        if result:
            user = result[0]
            return {
                "id": user[0],
                "pin": user[1],
                "name": user[2],
                "role": user[3],
            }
        else:
            print("User not found.")
            return None
