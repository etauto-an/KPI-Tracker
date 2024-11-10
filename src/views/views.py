# src/views/views.py

def display_manager_menu():
    """
    Displays the manager menu options to the user.
    """
    print(
        "Manager Menu:\n"
        "1. Add Sales Rep\n"
        "2. View All KPIs\n"
        "3. Generate report\n"
        "4. Exit"
    )


def display_sales_rep_menu():
    """
    Displays the sales rep menu options to the user.
    """
    print(
        "Sales Rep Menu:\n"
        "1. Add Daily Metrics\n"
        "2. View Personal KPIs\n"
        "3. Logout"
    )


def prompt_for_metrics():
    """
    Prompts the user to enter daily metrics data.
    
    Returns:
        tuple: A tuple containing the following metrics:
            - scheduled_calls (int): Number of scheduled calls.
            - live_calls (int): Number of live calls.
            - offers (int): Number of offers made.
            - closed (int): Number of closed deals.
            - cash_collected (float): Amount of cash collected.
            - contract_value (float): Total contract value.
    """
    scheduled_calls = int(input("Enter scheduled calls: "))
    live_calls = int(input("Enter live calls: "))
    offers = int(input("Enter offers made: "))
    closed = int(input("Enter closed deals: "))
    cash_collected = float(input("Enter cash collected: "))
    contract_value = float(input("Enter contract value: "))
    
    # Return all the collected metrics as a tuple
    return (
        scheduled_calls,
        live_calls,
        offers,
        closed,
        cash_collected,
        contract_value,
    )
