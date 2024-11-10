# src/models/kpi_calculator.py

from .sales_rep_data import SalesRepData
from .user_manager import UserManager


class KPI:
    """
    Calculates KPIs for sales reps, allowing performance comparison across all
    reps.
    """

    def __init__(self, db, user_manager: UserManager):
        """
        Initializes KPI with database and user manager instances.

        Args:
            db (Database): Instance of the Database class for data operations.
            user_manager (UserManager): UserManager instance to retrieve sales
            reps.
        """
        self.db = db
        self.user_manager = user_manager

    def calculate_kpis(self, rep_id, name):
        """
        Calculates KPIs (Key Performance Indicators) for a specific sales rep.

        Args:
            rep_id (int): The ID of the sales rep.
            name (str): The name of the sales rep.

        Outputs:
            Displays KPI summary including show percentage, offer percentage,
            close percentage, cash per call, and revenue per call.
        """
        # Fetch sales rep data from sales_rep_data table
        data = self.db.fetch_all(
            """
            SELECT SUM(scheduled_calls), SUM(live_calls), SUM(offers), 
                   SUM(closed), SUM(cash_collected), SUM(contract_value)
            FROM sales_rep_data
            WHERE rep_id = ?
            """,
            (rep_id,),
        )[0]

        # Calculate KPIs
        # (Detailed KPI calculations here)

        # Output KPI summary for the given sales rep
        print(f"\nKPI Summary for {name}:\n")
        # (Display each calculated KPI)

    def compare_all_kpis(self):
        """
        Compares KPIs across all sales reps by retrieving data through
        UserManager.

        Outputs:
            Displays a KPI summary for each sales rep for comparison.
        """
        # Get all sales reps from UserManager
        reps = [
            user
            for user in self.user_manager.get_all_users()
            if user["role"] == "sales_rep"
        ]

        # Compare KPIs for each sales rep
        for rep in reps:
            self.calculate_kpis(rep["id"], rep["name"])
