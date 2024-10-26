# kpi_calculator.py
from database import Database


class KPI:
    """
    Calculates KPIs for sales reps, including show %, offer %, close %,
    cash per call, and revenue per call. Also provides comparisons across reps.
    """

    def __init__(self, db: Database):
        # Reference to the Database instance
        self.db = db

    def calculate_kpis(self, rep_id, name):
        """
        Calculates KPIs for a specific sales rep identified by rep_id.
        Outputs the results to the console.
        """
        data = self.db.fetch_all(
            """
            SELECT SUM(scheduled_calls), SUM(live_calls), SUM(offers), 
                   SUM(closed), SUM(cash_collected), SUM(contract_value)
            FROM sales_rep_data
            WHERE rep_id = ?
        """,
            (rep_id,),
        )[0]

        # Unpack data and check for availability
        (
            total_scheduled_calls,
            total_live_calls,
            total_offers,
            total_closed,
            total_cash_collected,
            total_contract_value,
        ) = data

        if not data or total_scheduled_calls is None:
            print(f"No data available for {name}.")
            return

        # Calculate KPIs
        show_percentage = (
            (total_live_calls / total_scheduled_calls) * 100
            if total_scheduled_calls > 0
            else 0
        )
        offer_percentage = (
            (total_offers / total_live_calls) * 100
            if total_live_calls > 0
            else 0
        )
        close_percentage = (
            (total_closed / total_offers) * 100 if total_offers > 0 else 0
        )
        cash_per_call = (
            total_cash_collected / total_live_calls
            if total_live_calls > 0
            else 0
        )
        revenue_per_call = (
            total_contract_value / total_live_calls
            if total_live_calls > 0
            else 0
        )

        # Print KPI report for this rep
        print(f"\nKPI Report for {name}:")
        print(f"Show %: {show_percentage:.2f}%")
        print(f"Offer %: {offer_percentage:.2f}%")
        print(f"Close %: {close_percentage:.2f}%")
        print(f"Cash per Call: ${cash_per_call:.2f}")
        print(f"Revenue per Call: ${revenue_per_call:.2f}")
        print(f"Total Cash Collected: ${total_cash_collected:.2f}")
        print(f"Total Contract Value: ${total_contract_value:.2f}")

    def compare_all_kpis(self):
        """
        Calculates and displays KPIs for all sales reps to allow
        performance comparison across the team.
        """
        # Fetch all sales reps
        reps = self.db.fetch_all("SELECT id, name FROM sales_rep")

        if not reps:
            print("No sales reps available for comparison.")
            return

        print("\nComparing KPIs Across All Sales Reps:")
        print("----------------------------------------------------")

        # Loop through each sales rep and calculate KPIs
        for rep_id, name in reps:
            print(f"\n{name}'s KPI Summary:")
            self.calculate_kpis(rep_id, name)
            print("----------------------------------------------------")
