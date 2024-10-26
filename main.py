# main.py
from database import Database
from sales_rep import SalesRep
from sales_rep_data import SalesRepData
from kpi_calculator import KPI


def main():
    """
    Main entry point for the KPI Tracker, providing a CLI menu
    to add sales reps, record metrics, calculate KPIs, and compare KPIs.
    """
    # Initialize database and related classes
    db = Database()
    sales_rep_manager = SalesRep(db)
    metrics_manager = SalesRepData(db)
    kpi_calculator = KPI(db)

    while True:
        # Display the main menu
        print("\nKPI Tracker Menu:")
        print("1. Add a new sales rep")
        print("2. Add daily metrics for a sales rep")
        print("3. Calculate KPIs for a sales rep")
        print("4. Compare KPIs across all sales reps")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Option to add a new sales rep
            name = input("Enter the new sales rep's name: ").strip()
            sales_rep_manager.add_sales_rep(name)
        elif choice == "2":
            # Option to add metrics for a selected sales rep
            selected_rep = sales_rep_manager.select_sales_rep()
            if selected_rep:
                metrics_manager.add_daily_metrics(selected_rep[0])
        elif choice == "3":
            # Option to calculate KPIs for a selected sales rep
            selected_rep = sales_rep_manager.select_sales_rep()
            if selected_rep:
                kpi_calculator.calculate_kpis(selected_rep[0], selected_rep[1])
        elif choice == "4":
            # Option to compare KPIs across all sales reps
            kpi_calculator.compare_all_kpis()
        elif choice == "5":
            # Exit the program
            print("Exiting KPI Tracker.")
            db.close()
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
