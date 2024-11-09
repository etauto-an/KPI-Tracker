from database import Database
from sales_rep import SalesRep
from sales_rep_data import SalesRepData
from kpi_calculator import KPI
from user_manager import UserManager
from menus import manager_menu, sales_rep_menu  # Import menus
import hashlib


# Define the initial_setup function
def initial_setup(user_manager):
    print("No users found in the database. Initial setup required.")
    print("Please create the first manager account.")

    name = input("Enter manager name: ").strip()
    user_id = input("Enter user ID (e.g., MGR001): ").strip()
    pin = input("Enter a secure PIN: ").strip()

    hashed_pin = hash_pin(pin)

    # Create the initial manager account
    user_manager.add_user(
        user_id=user_id, pin=hashed_pin, name=name, role="manager"
    )
    print(f"Manager account created successfully with ID {user_id}.")


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def main():
    # Initialize database and related classes
    db = Database()
    sales_rep_manager = SalesRep(db)
    metrics_manager = SalesRepData(db)
    kpi_calculator = KPI(db)
    user_manager = UserManager(db)

    # Check if any users exist in the database
    users_exist = db.fetch_all("SELECT * FROM users")

    if not users_exist:
        initial_setup(user_manager)
    else:
        user_id = input("Enter your User ID: ").strip()
        pin = input("Enter your PIN: ").strip()
        hashed_pin = hash_pin(pin)
        user = user_manager.get_user(user_id)

        if user and user["pin"] == hashed_pin:
            print(
                f"Welcome, {user['name']}! You are logged in as a {user['role']}."
            )
            if user["role"] == "manager":
                manager_menu(
                    user_manager,
                    sales_rep_manager,
                    metrics_manager,
                    kpi_calculator,
                )
            elif user["role"] == "sales_rep":
                sales_rep_menu(user_id, metrics_manager, kpi_calculator)
        else:
            print("Invalid User ID or PIN. Please try again.")

    db.close()


if __name__ == "__main__":
    main()
