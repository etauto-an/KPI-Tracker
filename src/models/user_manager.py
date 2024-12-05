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

    def add_user(self, user_id, name, pin, role="sales_rep"):
        """
        Adds a new user to the system with the given details.

        Args:
            user_id (str): Unique identifier for the user (e.g., "SR001").
            name (str): Name of the user.
            pin (str): Hashed PIN for the user's login.
            role (str): Role of the user, defaults to "sales_rep".

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
                   (True, "Success message") if the user is added successfully.
                   (False, "Error message") if the operation fails (e.g., duplicate ID).
        """
        response = self.db.insert_user(user_id, name, pin, role)
        if response["success"]:
            return True, response["message"]
        else:
            return False, response["message"]

    def get_user(self, user_id):
        """
        Retrieves user information based on the provided user ID.

        Args:
            user_id (str): The user ID to retrieve information for.

        Returns:
            dict: A dictionary with the user's details (id, pin, name, role)
                  if the user exists. Returns None if the user is not found.
        """
        result = self.db.fetch_all(
            """
            SELECT id, pin, name, role FROM users WHERE id = ?
            """,
            (user_id,),
        )
        if result:
            # Return the user data as a dictionary
            return {
                "id": result[0][0],  # User ID
                "pin": result[0][1],  # Hashed PIN
                "name": result[0][2],  # User's name
                "role": result[0][3],  # User's role
            }
        return None  # User not found

    def get_all_users(self):
        """
        Retrieves all users in the system. Mainly used for administrative tasks
        like KPI calculations or viewing user lists.

        Returns:
            list: A list of dictionaries containing user information (id, name, role)
                  for all users in the database.
        """
        results = self.db.fetch_all("SELECT id, name, role FROM users")
        # Convert the query result into a list of dictionaries
        return [
            {"id": row[0], "name": row[1], "role": row[2]} for row in results
        ]
