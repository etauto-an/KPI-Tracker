# main.py

from src.models.database import Database
from src.models.sales_rep_data import SalesRepData
from src.models.kpi_calculator import KPI
from src.models.user_manager import UserManager
from src.controllers.menus import manager_menu, sales_rep_menu
import hashlib


def hash_pin(pin):
    """
    Hashes a user's PIN for secure storage and comparison.

    Args:
        pin (str): Plain text PIN to hash.

    Returns:
        str: SHA-256 hash of the PIN.
    """
    return hashlib.sha256(pin.encode()).hexdigest()


def initial_setup(user_manager):
    """
    Initializes the database with an initial manager account if no users
    exist.

    Args:
        user_manager (UserManager): Instance of UserManager to manage users.
    """
    print("No users found in the database. Initial setup required.")
    print("Please create the first manager account.")

    name = input("Enter manager name: ").strip()
    user_id = input("Enter user ID (e.g., MGR001): ").strip()
    pin = input("Enter a 4-digit PIN: ").strip()

    hashed_pin = hash_pin(pin)

    # Create the initial manager account
    user_manager.add_user(
        user_id=user_id, pin=hashed_pin, name=name, role="manager"
    )
    print(f"Manager account created successfully with ID {user_id}.")


def main():
    # Initialize database and related classes
    db = Database()
    user_manager = UserManager(db)
    metrics_manager = SalesRepData(db)
    kpi_calculator = KPI(db, user_manager)

    # Check if any users exist in the database
    users_exist = db.fetch_all("SELECT * FROM users")

    if not users_exist:
        # Perform initial setup and directly enter the manager menu afterward
        initial_setup(user_manager)
        print("Logging in as the initial manager...")
        manager_menu(user_manager, metrics_manager, kpi_calculator)
    else:
        # Prompt for login if users already exist
        user_id = input("Enter your User ID: ").strip()
        pin = input("Enter your PIN: ").strip()
        print("")
        hashed_pin = hash_pin(pin)

        user = user_manager.get_user(user_id)

        if user and user["pin"] == hashed_pin:
            print(
                f"Welcome, {user['name']}! You are logged in as a "
                f"{user['role']}."
            )

            # Determine which menu to show based on role
            if user["role"] == "manager":
                manager_menu(user_manager, metrics_manager, kpi_calculator)
            elif user["role"] == "sales_rep":
                sales_rep_menu(
                    metrics_manager, kpi_calculator, user_id, user["name"]
                )
        else:
            print("Invalid User ID or PIN. Please try again.")

    db.close()


if __name__ == "__main__":
    main()
