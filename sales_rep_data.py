# sales_rep_data.py
from database import Database
from datetime import datetime


class SalesRepData:
    """
    Manages daily metrics for each sales representative.
    Allows adding data like calls, offers, closed deals, etc.
    """

    def __init__(self, db: Database):
        # Reference to the Database instance
        self.db = db

    def add_daily_metrics(self, rep_id):
        """
        Adds daily metrics for a specific sales rep (identified by rep_id).
        """
        try:
            # Gather inputs for each metric
            scheduled_calls = int(input("Enter scheduled calls: "))
            live_calls = int(input("Enter live calls: "))
            offers = int(input("Enter offers: "))
            closed = int(input("Enter closed deals: "))
            cash_collected = float(input("Enter cash collected: "))
            contract_value = float(input("Enter contract value: "))

            # Get current date for the entry
            date = datetime.now().strftime("%Y-%m-%d")

            # Insert metrics into sales_rep_data table
            self.db.execute_query(
                """
                INSERT INTO sales_rep_data 
                (rep_id, date, scheduled_calls, live_calls, offers, closed, 
                cash_collected, contract_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    rep_id,
                    date,
                    scheduled_calls,
                    live_calls,
                    offers,
                    closed,
                    cash_collected,
                    contract_value,
                ),
            )
            print(f"Metrics for sales rep ID {rep_id} added successfully.")
        except ValueError:
            print("Invalid input. Enter valid numbers for metrics.")
