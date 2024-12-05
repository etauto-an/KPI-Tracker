# src/controllers/menus.py

from src.views import views
from src.models.user_manager import UserManager
from src.models.sales_rep_data import SalesRepData
from src.models.kpi_calculator import KPI
from src.controllers.utils import (
    get_nonempty_input,
    get_numeric_input,
    hash_pin,
    clear_screen,
    seed_database,
    seed_database_interactive,
    generate_report,
)
import os


def login_user(user_manager):
    """
    Prompts the user for login credentials and authenticates the user.

    Args:
        user_manager (UserManager): Instance of UserManager to handle user authentication.

    Returns:
        dict: User details if authentication is successful, None otherwise.
    """
    user_id = input("Enter your User ID: ").strip()
    pin = input("Enter your PIN: ").strip()
    clear_screen()
    hashed_pin = hash_pin(pin)

    user = user_manager.get_user(user_id)

    if user and user["pin"] == hashed_pin:
        print(
            f"Welcome, {user['name']}! You are logged in as a {user['role']}."
        )
        return user
    else:
        print("Invalid User ID or PIN.")
        return None


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
    import plotext as plt  # Import plotext for graphing

    while True:
        views.display_manager_menu()
        choice = input("Enter your choice: ").strip()
        clear_screen()  # Clear the terminal before displaying the menu

        if choice == "1":
            # Add a new sales rep using UserManager
            name = get_nonempty_input("Enter the sales rep's name: ")
            user_id = get_nonempty_input(
                "Enter the sales rep's user ID (e.g., SR001): "
            )

            # Use get_numeric_input to enforce nonempty and numeric validation for PIN
            pin = get_numeric_input(
                "Enter a 4-digit PIN for the sales rep: ", length=4
            )

            hashed_pin = hash_pin(pin)
            clear_screen()

            # Use UserManager's insert_user method to add the new sales rep
            result = user_manager.db.insert_user(
                user_id=user_id, name=name, pin=hashed_pin, role="sales_rep"
            )

            if result["success"]:
                print(f"Sales rep {name} added successfully with ID {user_id}.")
            else:
                print(f"Error: {result['message']}")

        elif choice == "2":
            # View KPIs across all sales reps using KPI
            print("Comparing KPIs Across All Sales Reps:")
            kpi_calculator.compare_all_kpis()

        elif choice == "3":
            # Generate team performance overview
            print("Generating report:")
            generate_report(metrics_manager)

        elif choice == "4":
            # Exit the manager menu
            print("Logging out of manager menu.")
            break

        elif choice == "5":
            # Seed the database with sample data
            seed_database_interactive(metrics_manager)

        else:
            print("Invalid choice. Please try again.")


def sales_rep_menu(
    metrics_manager: SalesRepData, kpi_calculator: KPI, rep_id: str, name: str
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
        clear_screen()  # Clear the terminal before displaying the menu

        if choice == "1":
            # Prompt for daily metrics and add them using SalesRepData
            (
                date,
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            ) = views.prompt_for_metrics()
            metrics_manager.add_daily_metrics(
                rep_id,
                date,
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            )
            clear_screen()
            print("Daily metrics added successfully.")

        elif choice == "2":
            # View personal KPIs using KPI calculator
            # print(f"\nKPI Summary for Sales Rep {rep_id}:")

            kpi_calculator.calculate_kpis(rep_id, name)

        elif choice == "3":
            # Exit the sales rep menu
            print("Logging out of sales rep menu.")
            break

        else:
            print("Invalid choice. Please try again.")


def initial_setup(user_manager):
    """
    Initializes the database with an initial manager account if no users exist.

    Args:
        user_manager (UserManager): Instance of UserManager to manage users.
    """
    print("No users found in the database. Initial setup required.")
    print("Please create the first manager account.")

    # Validate nonempty input for name, user_id, and PIN
    name = get_nonempty_input("Enter manager name: ")
    user_id = get_nonempty_input("Enter user ID (e.g., MGR001): ")
    pin = get_numeric_input("Enter a 4-digit PIN: ")
    clear_screen()
    hashed_pin = hash_pin(pin)

    # Create the initial manager account
    user_manager.add_user(
        user_id=user_id, pin=hashed_pin, name=name, role="manager"
    )
    print(f"Manager account created successfully with ID {user_id}.")
