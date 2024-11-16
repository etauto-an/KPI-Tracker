# src/controllers/menus.py

from src.views import views
from src.models.user_manager import UserManager
from src.models.sales_rep_data import SalesRepData
from src.models.kpi_calculator import KPI
import os


def clear_screen():
    # Check if the OS is Windows or Unix/Linux/Mac and clear screen accordingly
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix/Linux/Mac
        os.system("clear")


def get_nonempty_input(prompt):
    """
    Prompts the user for input and ensures the input is not empty.

    Args:
        prompt (str): The input prompt to display.

    Returns:
        str: The valid, nonempty input provided by the user.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: All fields are required. Please enter valid data.")


def get_numeric_input(prompt, length=4):
    """
    Prompts the user for numeric input and ensures it contains only digits and has the required length.

    Args:
        prompt (str): The input prompt to display.
        length (int, optional): The required length of the input. Defaults to None.

    Returns:
        str: A valid numeric input.
    """
    while True:
        value = input(prompt).strip()
        if value.isdigit():  # Ensures input is numeric and nonempty
            if length and len(value) != length:
                print(
                    f"Error: Input must be exactly {length} digits. Please try again."
                )
            else:
                return value  # Valid numeric input with the correct length
        else:
            print(
                "Error: Input must be numeric and not empty. Please try again."
            )


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
        clear_screen()  # Clear the terminal before displaying the menu

        if choice == "1":
            # Add a new sales rep using UserManager
            name = get_nonempty_input("Enter the sales rep's name: ")
            while True:
                user_id = get_nonempty_input(
                    "Enter the sales rep's user ID (e.g., SR001): "
                )
                if user_manager.validate_user_id(user_id):
                    break  # Exit the loop if the User ID is unique
                print(
                    f"Error: User ID '{user_id}' already exists. Please try a different ID."
                )

            # Use get_numeric_input to enforce nonempty and numeric validation for PIN
            pin = get_numeric_input(
                "Enter a 4-digit PIN for the sales rep: ", length=4
            )

            hashed_pin = hash_pin(pin)

            # Use UserManager to add the new sales rep
            try:
                user_manager.add_user(
                    user_id=user_id, pin=hashed_pin, name=name, role="sales_rep"
                )
                print(f"Sales rep {name} added successfully with ID {user_id}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            # View KPIs across all sales reps using KPI
            print("\nComparing KPIs Across All Sales Reps:")
            kpi_calculator.compare_all_kpis()

        elif choice == "3":
            # Placeholder for report generation
            print("Generating report (functionality to be implemented).")
            print("")

        elif choice == "4":
            # Exit the manager menu
            print("Logging out of manager menu.")
            break

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
            # print(f"\nKPI Summary for Sales Rep {rep_id}:")

            kpi_calculator.calculate_kpis(rep_id, name)

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
