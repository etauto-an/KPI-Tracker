# menus.py
import hashlib
from kpi_calculator import KPI


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def manager_menu(
    user_manager, sales_rep_manager, metrics_manager, kpi_calculator
):
    while True:
        print("\nManager Menu:")
        print("1. Add New Sales Rep")
        print("2. View All Sales Reps’ KPIs")
        print("3. Generate Reports")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter the sales rep's name: ").strip()
            user_id = input("Enter the sales rep's user ID: ").strip()
            pin = hash_pin(input("Enter a PIN for the sales rep: ").strip())
            user_manager.add_user(user_id, pin, name, role="sales_rep")
        elif choice == "2":
            KPI.compare_all_kpis()
        elif choice == "3":
            print("Generating report (functionality to be implemented).")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def sales_rep_menu(rep_id, metrics_manager, kpi_calculator):
    while True:
        print("\nSales Rep Menu:")
        print("1. Add Daily Metrics")
        print("2. View Personal KPIs")
        print("3. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            metrics_manager.add_daily_metrics(rep_id)
        elif choice == "2":
            name = "Sales Rep"  # Placeholder name if necessary
            kpi_calculator.calculate_kpis(rep_id, name)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
