# sales_rep_data.py
from .database import Database
from datetime import datetime


class SalesRepData:
    """
    Manages daily metrics for each sales representative.
    Allows adding data like calls, offers, closed deals, etc.
    """

    def __init__(self, db: Database):
        # Reference to the Database instance
        self.db = db

    def add_daily_metrics(
        self,
        rep_id,
        date,
        scheduled_calls,
        live_calls,
        offers,
        closed,
        cash_collected,
        contract_value,
    ):
        """
        Adds daily metrics for a specific sales rep to the database.

        Args:
            rep_id (str): The ID of the sales rep.
            date (str): The date of the metrics in MM/DD/YYYY format.
            scheduled_calls (int): The number of scheduled calls.
            live_calls (int): The number of live calls.
            offers (int): The number of offers made.
            closed (int): The number of closed deals.
            cash_collected (float): The amount of cash collected.
            contract_value (float): The value of contracts closed.
        """
        self.db.execute_query(
            """
            INSERT INTO sales_rep_data (
                rep_id, date, scheduled_calls, live_calls, offers,
                closed, cash_collected, contract_value
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rep_id,
                date,  # Explicitly use the provided date
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            ),
        )
