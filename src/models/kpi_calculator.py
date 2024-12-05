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
            Displays KPI summary including raw values, show percentage, offer
            percentage, close percentage, cash per call, and revenue per call in
            the specified format.
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

        # Unpack data
        (
            scheduled_calls,
            live_calls,
            offers,
            closed,
            cash_collected,
            contract_value,
        ) = data

        # Calculate KPIs with conditional handling to avoid division by zero
        show_percentage = (
            (live_calls / scheduled_calls * 100) if scheduled_calls else 0
        )
        offer_percentage = (offers / live_calls * 100) if live_calls else 0
        close_percentage = (closed / offers * 100) if offers else 0
        cash_per_call = (cash_collected / live_calls) if live_calls else 0
        revenue_per_call = (contract_value / live_calls) if live_calls else 0

        # Output KPI summary for the given sales rep
        print(f"\nKPI Summary for Employee {rep_id}:")
        print(
            f" - Show Percentage: {show_percentage:.2f}% ({scheduled_calls} "
            f"Scheduled Calls, {live_calls} Live Calls)"
        )
        print(
            f" - Offer Percentage: {offer_percentage:.2f}% ({live_calls} Live Calls, "
            f"{offers} Offers)"
        )
        print(
            f" - Close Percentage: {close_percentage:.2f}% ({offers} Offers, {closed} "
            f"Closed Deals)"
        )
        print(f" - Cash Collected: ${cash_collected:.2f}")
        print(f" - Contract Value: ${contract_value:.2f}")

    def compare_all_kpis(self):
        """
        Compares KPIs across all sales reps by retrieving data through
        UserManager.

        Outputs:
            Displays a KPI summary (with raw values) for each sales rep for
            comparison.
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
