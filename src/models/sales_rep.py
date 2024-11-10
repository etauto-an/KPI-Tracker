# sales_rep.py
import sqlite3
from .database import Database


class SalesRep:
    """
    Manages sales reps in the database: adding reps and listing all reps.
    """

    def __init__(self, db: Database):
        self.db = db

    def add_sales_rep(self, name):
        """
        Adds a new sales rep. The employee ID is auto-generated and displayed in the format EMP001.
        """
        try:
            # Execute the query to insert the new sales rep
            self.db.execute_query(
                "INSERT INTO sales_rep (name) VALUES (?)", (name,)
            )
            # Fetch the ID of the newly added sales rep
            rep_id = self.db.cursor.lastrowid
            # Format the ID as EMP001, EMP002, etc.
            formatted_id = f"EMP{rep_id:03d}"
            print(
                f"Sales rep {name} added successfully with ID: {formatted_id}."
            )
        except sqlite3.IntegrityError:
            print("An error occurred while adding the sales rep.")

    def get_all_sales_reps(self):
        """
        Fetches all sales reps and returns a list of tuples (id, name).
        """
        return self.db.fetch_all("SELECT id, name FROM sales_rep")

    def select_sales_rep(self):
        """
        Lists all reps and allows user to select one by ID.
        Returns (id, name) of the selected rep.
        """
        reps = self.get_all_sales_reps()
        if not reps:
            print("No reps found. Please add a new sales rep first.")
            return None

        print("\nAvailable Sales Reps:")
        for rep in reps:
            print(f"{rep[0]}. {rep[1]}")

        try:
            rep_id = int(input("\nEnter the sales rep's ID: "))
            return next((r for r in reps if r[0] == rep_id), None)
        except ValueError:
            print("Invalid input. Please enter a numeric ID.")
            return None

    def select_sales_rep_by_id(self, rep_id):
        """
        Selects a sales rep by a given ID and returns the (id, name) tuple.
        """
        rep = self.db.fetch_all(
            "SELECT id, name FROM sales_rep WHERE id = ?", (rep_id,)
        )
        return rep[0] if rep else None
