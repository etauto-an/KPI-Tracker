# src/controllers/menus.py

from src.views import views
from src.models.user_manager import UserManager
from src.models.sales_rep_data import SalesRepData
from src.models.kpi_calculator import KPI


def manager_menu(
    user_manager: UserManager,
    metrics_manager: SalesRepData,
    kpi_calculator: KPI,
):
    """
    Displays the manager menu and handles manager-specific actions.

    Args:
        user_manager (UserManager): Instance of UserManager for managing users.
        metrics_manager (SalesRepData): Instance of SalesRepData for metrics
        management.
        kpi_calculator (KPI): Instance of KPI for KPI calculations.
    """
    while True:
        views.display_manager_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Add a new sales rep using UserManager
            name = input("Enter the sales rep's name: ").strip()
            user_id = input(
                "Enter the sales rep's user ID (e.g., SR001): "
            ).strip()
            pin = input("Enter a PIN for the sales rep: ").strip()
            hashed_pin = hash_pin(pin)

            # Use UserManager to add the new sales rep
            user_manager.add_user(
                user_id=user_id, pin=hashed_pin, name=name, role="sales_rep"
            )
            print(f"Sales rep {name} added successfully with ID {user_id}.")

        elif choice == "2":
            # View KPIs across all sales reps using KPI
            print("\nComparing KPIs Across All Sales Reps:")
            kpi_calculator.compare_all_kpis()

        elif choice == "3":
            # Placeholder for report generation
            print("Generating report (functionality to be implemented).")

        elif choice == "4":
            # Exit the manager menu
            print("Logging out of manager menu.")
            break

        else:
            print("Invalid choice. Please try again.")


def sales_rep_menu(
    metrics_manager: SalesRepData, kpi_calculator: KPI, rep_id: str
):
    """
    Displays the sales rep menu and handles sales rep-specific actions.

    Args:
        metrics_manager (SalesRepData): Instance of SalesRepData for managing
        daily metrics.
        kpi_calculator (KPI): Instance of KPI for calculating personal KPIs.
        rep_id (str): The ID of the sales rep.
    """
    while True:
        views.display_sales_rep_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Prompt for daily metrics and add them using SalesRepData
            (
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            ) = views.prompt_for_metrics()
            metrics_manager.add_daily_metrics(
                rep_id,
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            )
            print("Daily metrics added successfully.")

        elif choice == "2":
            # View personal KPIs using KPI calculator
            print(f"\nKPI Summary for Sales Rep {rep_id}:")
            kpi_calculator.calculate_kpis(rep_id, "Your Name")

        elif choice == "3":
            # Exit the sales rep menu
            print("Logging out of sales rep menu.")
            break

        else:
            print("Invalid choice. Please try again.")


def hash_pin(pin):
    """
    Hashes a user's PIN for secure storage and comparison.

    Args:
        pin (str): Plain text PIN to hash.

    Returns:
        str: SHA-256 hash of the PIN.
    """
    import hashlib

    return hashlib.sha256(pin.encode()).hexdigest()
