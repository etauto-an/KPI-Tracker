# sales_rep.py
import sqlite3
from database import Database


class SalesRep:
    """
    Manages sales reps in the database: adding reps and listing all reps.
    """

    def __init__(self, db: Database):
        # Reference to the Database instance
        self.db = db

    def add_sales_rep(self, name):
        """
        Adds a new sales rep by name. Ensures names are unique.
        """
        try:
            # Insert new rep into the sales_rep table
            self.db.execute_query(
                "INSERT INTO sales_rep (name) VALUES (?)", (name,)
            )
            print(f"Sales rep {name} added successfully.")
        except sqlite3.IntegrityError:
            print(f"Sales rep {name} already exists. Enter a unique name.")

    def get_all_sales_reps(self):
        """
        Fetches all sales reps from the database.
        Returns a list of tuples with (id, name).
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
