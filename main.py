# main.py

from src.models.database import Database
from src.models.sales_rep_data import SalesRepData
from src.models.kpi_calculator import KPI
from src.models.user_manager import UserManager
from src.controllers.menus import (
    manager_menu,
    sales_rep_menu,
    initial_setup,
    login_user,
)


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
        # Prompt for login
        user = login_user(user_manager)

        if user:
            # Determine which menu to show based on role
            if user["role"] == "manager":
                manager_menu(user_manager, metrics_manager, kpi_calculator)
            elif user["role"] == "sales_rep":
                sales_rep_menu(
                    metrics_manager, kpi_calculator, user["id"], user["name"]
                )
            else:
                print("Invalid User Role. Please contact your administrator.")
        else:
            print("Login failed. Please try again.")

    db.close()


if __name__ == "__main__":
    main()
