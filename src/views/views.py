# src/views/views.py
from src.controllers.utils import get_numeric_input_metrics, get_valid_date


def display_manager_menu():
    """
    Displays the manager menu options to the user.
    """
    print(
        "\nManager Menu:\n"
        "1. Add Sales Rep\n"
        "2. View All KPIs\n"
        "3. Generate report\n"
        "4. Exit\n"
        "5. Seed DB with Sample Data\n"
    )


def display_sales_rep_menu():
    """
    Displays the sales rep menu options to the user.
    """
    print(
        "\nSales Rep Menu:\n"
        "1. Add Daily Metrics\n"
        "2. View Personal KPIs\n"
        "3. Logout\n"
    )
    # print("")


def prompt_for_metrics():
    """
    Prompts the user to enter daily metrics data and a date with validation.

    Returns:
        tuple: A tuple containing the following validated metrics:
            - date (str): The date for the metrics in YYYY-MM-DD format.
            - scheduled_calls (int): Number of scheduled calls.
            - live_calls (int): Number of live calls.
            - offers (int): Number of offers made.
            - closed (int): Number of closed deals.
            - cash_collected (float): Amount of cash collected.
            - contract_value (float): Total contract value.
    """
    date = get_valid_date("Enter the date (YYYY-MM-DD): ")
    scheduled_calls = int(get_numeric_input_metrics("Enter scheduled calls: "))
    live_calls = int(get_numeric_input_metrics("Enter live calls: "))
    offers = int(get_numeric_input_metrics("Enter offers made: "))
    closed = int(get_numeric_input_metrics("Enter closed deals: "))
    cash_collected = float(get_numeric_input_metrics("Enter cash collected: "))
    contract_value = float(get_numeric_input_metrics("Enter contract value: "))

    return (
        date,
        scheduled_calls,
        live_calls,
        offers,
        closed,
        cash_collected,
        contract_value,
    )
