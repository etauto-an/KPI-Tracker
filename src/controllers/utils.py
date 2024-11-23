import os
import random
import statistics
from datetime import datetime, timedelta


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
        clear_screen()


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


def get_numeric_input_metrics(prompt):
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
            return value  # Valid numeric input with the correct length
        else:
            print(
                "Error: Input must be numeric and not empty. Please try again."
            )


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


def get_valid_date(prompt):
    """
    Prompts the user to input a date in the format YYYY-MM-DD and validates it.

    Args:
        prompt (str): The input prompt to display.

    Returns:
        str: A valid date string in the format YYYY-MM-DD.
    """
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            print("Error: Date cannot be empty. Please enter a valid date.")
            continue
        try:
            # Parse and ensure the input date is valid
            valid_date = datetime.strptime(date_str, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")  # Return consistent format
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")


def seed_database_interactive(metrics_manager):
    """
    Interactively seeds the database with sample employee data and metrics.

    Args:
        metrics_manager (SalesRepData): Instance of SalesRepData for database operations.
    """
    try:
        # Prompt for the number of employees and days
        employee_count = int(
            get_numeric_input(
                "Enter the number of employees to generate: ", length=None
            )
        )
        days = int(
            get_numeric_input(
                "Enter the number of days to generate data for: ", length=None
            )
        )
        start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")

        # Seed the database
        employee_ids = seed_database(
            metrics_manager.db,
            employee_count=employee_count,
            start_date=start_date,
            days=days,
        )
        print(
            f"Database successfully seeded with {len(employee_ids)} employees and {days} days of data."
        )
    except ValueError as e:
        print(f"Error: {e}. Please try again.")


def seed_database(db, employee_count, start_date, days):
    """
    Seeds the database with a given number of employees and days of metrics.

    Args:
        db (Database): The database instance.
        employee_count (int): Number of employees to generate data for.
        start_date (str): Starting date in 'YYYY-MM-DD' format.
        days (int): Number of days to generate metrics for.

    Returns:
        list: A list of generated employee IDs.
    """
    # Parse the start_date in YYYY-MM-DD format
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    # Generate employee IDs
    employee_ids = [f"SR{str(i+1).zfill(3)}" for i in range(employee_count)]

    # Add employees to the database
    for employee_id in employee_ids:
        db.execute_query(
            """
            INSERT INTO users (id, pin, name, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                employee_id,
                "hashed_pin",  # Replace with actual hashed PIN if needed
                f"Employee {employee_id}",  # Name based on ID
                "sales_rep",
            ),
        )

    # Add metrics for each employee over the specified number of days
    for employee_id in employee_ids:
        for day in range(days):
            date = start_date + timedelta(days=day)
            scheduled_calls = random.randint(10, 50)
            live_calls = random.randint(5, scheduled_calls)
            offers = random.randint(2, live_calls)
            closed = random.randint(1, offers)
            cash_collected = round(random.uniform(100.0, 1000.0), 2)
            contract_value = round(cash_collected * random.uniform(1.1, 2.0), 2)

            db.execute_query(
                """
                INSERT INTO sales_rep_data (
                    rep_id, date, scheduled_calls, live_calls, offers,
                    closed, cash_collected, contract_value
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    date.strftime(
                        "%Y-%m-%d"
                    ),  # Convert to database-friendly format
                    scheduled_calls,
                    live_calls,
                    offers,
                    closed,
                    cash_collected,
                    contract_value,
                ),
            )

    return employee_ids


def generate_report(metrics_manager):
    """
    Generates a textual report summarizing the team's performance,
    including team-wide averages, quartile statistics, underperforming reps, and top performers.

    Args:
        metrics_manager (SalesRepData): Instance of SalesRepData for fetching metrics.
    """
    # Prompt for date range
    start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    end_date = get_valid_date("Enter the end date (YYYY-MM-DD): ")
    clear_screen()

    # Fetch all data for the specified date range
    data = metrics_manager.db.fetch_all(
        """
        SELECT rep_id, SUM(scheduled_calls) AS scheduled_calls, 
               SUM(live_calls) AS live_calls, SUM(offers) AS offers, 
               SUM(closed) AS closed, SUM(cash_collected) AS cash_collected, 
               SUM(contract_value) AS contract_value
        FROM sales_rep_data
        WHERE date BETWEEN ? AND ?
        GROUP BY rep_id
        """,
        (start_date, end_date),
    )

    if not data:
        print(f"No performance data found between {start_date} and {end_date}.")
        return

    # Initialize statistics
    team_totals = {
        "scheduled_calls": [],
        "live_calls": [],
        "offers": [],
        "closed": [],
        "cash_collected": [],
        "contract_value": [],
    }
    top_performers = {metric: None for metric in team_totals}
    top_values = {metric: 0 for metric in team_totals}

    # Populate team totals and identify top performers
    for entry in data:
        (
            rep_id,
            scheduled_calls,
            live_calls,
            offers,
            closed,
            cash_collected,
            contract_value,
        ) = entry

        # Add to team totals
        team_totals["scheduled_calls"].append(scheduled_calls)
        team_totals["live_calls"].append(live_calls)
        team_totals["offers"].append(offers)
        team_totals["closed"].append(closed)
        team_totals["cash_collected"].append(cash_collected)
        team_totals["contract_value"].append(contract_value)

        # Check for top performers
        for metric in team_totals:
            value = locals()[metric]
            if value > top_values[metric]:
                top_values[metric] = value
                top_performers[metric] = rep_id

    # Calculate averages and quartiles
    num_reps = len(data)
    team_averages = {
        metric: sum(values) / num_reps for metric, values in team_totals.items()
    }
    quartiles = {
        metric: {
            "Min": min(values),
            "Q1": statistics.quantiles(values, n=4)[0],
            "Median": statistics.median(values),
            "Q3": statistics.quantiles(values, n=4)[2],
            "Max": max(values),
            "Mean": team_averages[metric],  # Add the mean
        }
        for metric, values in team_totals.items()
    }

    # Identify underperforming reps
    underperformers = []
    for entry in data:
        (
            rep_id,
            scheduled_calls,
            live_calls,
            offers,
            closed,
            cash_collected,
            contract_value,
        ) = entry
        for metric, q1 in {k: v["Q1"] for k, v in quartiles.items()}.items():
            value = locals()[metric]
            if value < q1:  # Flag if below Q1
                underperformers.append(
                    f" - {rep_id}: {metric.replace('_', ' ').title()} ({value:.2f}, below Q1: {q1:.2f})"
                )

    # Generate team summary
    summary = [
        f"Team Performance Report ({start_date} to {end_date})",
        "=" * 50,
        "Team-Wide Averages:",
    ]
    for metric, average in team_averages.items():
        summary.append(f" - {metric.replace('_', ' ').title()}: {average:.2f}")

    summary.append("")
    summary.append("Quartile Statistics (Per Metric):")
    for metric, stats in quartiles.items():
        summary.append(f" - {metric.replace('_', ' ').title()}:")
        summary.append(f"   - Min: {stats['Min']:.2f}")
        summary.append(f"   - Q1: {stats['Q1']:.2f}")
        summary.append(f"   - Median: {stats['Median']:.2f}")
        summary.append(f"   - Q3: {stats['Q3']:.2f}")
        summary.append(f"   - Max: {stats['Max']:.2f}")
        summary.append(f"   - Mean: {stats['Mean']:.2f}")
        summary.append("")

    if underperformers:
        summary.append("Underperforming Reps:")
        summary.extend(underperformers)
    else:
        summary.append("No underperforming reps identified.")

    summary.append("")
    summary.append("Top Performers:")
    for metric, rep_id in top_performers.items():
        summary.append(
            f" - {metric.replace('_', ' ').title()}: {rep_id} ({top_values[metric]:.2f})"
        )

    # Combine and print the report
    print("\n".join(summary))
