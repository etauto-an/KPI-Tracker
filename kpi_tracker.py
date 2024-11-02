import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect("kpi_tracker_v2.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sales_rep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sales_rep_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rep_id INTEGER,
    date TEXT,
    scheduled_calls INTEGER,
    live_calls INTEGER,
    offers INTEGER,
    closed INTEGER,
    cash_collected REAL,
    contract_value REAL,
    FOREIGN KEY (rep_id) REFERENCES sales_rep (id)
)
"""
)
conn.commit()


# Function to add a new sales rep
def add_sales_rep():
    name = input("Enter the new sales rep's name: ").strip()
    try:
        cursor.execute("INSERT INTO sales_rep (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Sales rep {name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Sales rep {name} already exists. Please enter a unique name.")


# Function to select a sales rep
def select_sales_rep():
    cursor.execute("SELECT id, name FROM sales_rep")
    reps = cursor.fetchall()

    if not reps:
        print("No sales reps found. Please add a new sales rep first.")
        return None

    print("\nAvailable Sales Reps:")
    for rep in reps:
        print(f"{rep[0]}. {rep[1]}")

    try:
        rep_id = int(input("\nEnter the sales rep's ID: "))
        cursor.execute("SELECT id, name FROM sales_rep WHERE id = ?", (rep_id,))
        selected_rep = cursor.fetchone()
        if selected_rep:
            return selected_rep
        else:
            print("Invalid ID. Please try again.")
            return None
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return None


# Function to add daily metrics for a sales rep
def add_daily_metrics(rep_id):
    try:
        scheduled_calls = int(input("Enter number of scheduled calls: "))
        live_calls = int(input("Enter number of live calls: "))
        offers = int(input("Enter number of offers: "))
        closed = int(input("Enter number of closed deals: "))
        cash_collected = float(input("Enter cash collected: "))
        contract_value = float(input("Enter contract value: "))

        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            """
            INSERT INTO sales_rep_data (rep_id, date, scheduled_calls, live_calls, offers, closed, cash_collected, contract_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                rep_id,
                date,
                scheduled_calls,
                live_calls,
                offers,
                closed,
                cash_collected,
                contract_value,
            ),
        )
        conn.commit()

        print(f"Metrics for sales rep ID {rep_id} added successfully.")
    except ValueError:
        print(
            "Invalid input. Please enter valid numbers for calls, offers, deals, cash, and contract values."
        )


# Function to calculate KPIs for a given sales rep
def calculate_kpis(rep_id, name):
    cursor.execute(
        """
        SELECT SUM(scheduled_calls), SUM(live_calls), SUM(offers), SUM(closed), SUM(cash_collected), SUM(contract_value)
        FROM sales_rep_data
        WHERE rep_id = ?
    """,
        (rep_id,),
    )

    data = cursor.fetchone()
    (
        total_scheduled_calls,
        total_live_calls,
        total_offers,
        total_closed,
        total_cash_collected,
        total_contract_value,
    ) = data

    if total_scheduled_calls is None or total_scheduled_calls == 0:
        print(f"No data available for {name}.")
        return

    # KPI calculations
    show_percentage = (
        (total_live_calls / total_scheduled_calls) * 100
        if total_scheduled_calls > 0
        else 0
    )
    offer_percentage = (
        (total_offers / total_live_calls) * 100 if total_live_calls > 0 else 0
    )
    close_percentage = (
        (total_closed / total_offers) * 100 if total_offers > 0 else 0
    )
    cash_per_call = (
        total_cash_collected / total_live_calls if total_live_calls > 0 else 0
    )
    revenue_per_call = (
        total_contract_value / total_live_calls if total_live_calls > 0 else 0
    )

    # Improved Metrics (could add more as needed)
    print(f"\nKPI Report for {name}:")
    print(f"Show %: {show_percentage:.2f}%")
    print(f"Offer %: {offer_percentage:.2f}%")
    print(f"Close %: {close_percentage:.2f}%")
    print(f"Cash per Call: ${cash_per_call:.2f}")
    print(f"Revenue per Call: ${revenue_per_call:.2f}")
    print(f"Total Cash Collected: ${total_cash_collected:.2f}")
    print(f"Total Contract Value: ${total_contract_value:.2f}")


# Function to compare KPIs across all sales reps
def compare_sales_reps():
    cursor.execute("SELECT id, name FROM sales_rep")
    reps = cursor.fetchall()

    if not reps:
        print("No sales reps found.")
        return

    for rep in reps:
        calculate_kpis(rep[0], rep[1])


# Improved Terminal Interface
def main():
    while True:
        print("\nKPI Tracker Menu:")
        print("1. Add a new sales rep")
        print("2. Add daily metrics for a sales rep")
        print("3. Calculate KPIs for a sales rep")
        print("4. Compare KPIs across all sales reps")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_sales_rep()
        elif choice == "2":
            selected_rep = select_sales_rep()
            if selected_rep:
                add_daily_metrics(selected_rep[0])
        elif choice == "3":
            selected_rep = select_sales_rep()
            if selected_rep:
                calculate_kpis(selected_rep[0], selected_rep[1])
        elif choice == "4":
            compare_sales_reps()
        elif choice == "5":
            print("Exiting KPI Tracker.")
            break
        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()

# Close the connection when done
conn.close()
