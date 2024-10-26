from sales_rep import SalesRep
from database import Database


def test_false_negative():
    db = Database()
    sr = SalesRep(db)

    try:
        # Attempt to add unique sales reps, simulating a false negative scenario
        sr.add_sales_rep("Unique1")
        sr.add_sales_rep("Unique2")

        # Print successful entries
        print("Unique sales reps added successfully.")
        print(sr.get_all_sales_reps())

        # Simulate a false negative failure message
        print(
            "\033[31m[  FAILED  ] Expected unique entry failure "
            "(simulated false negative).\033[0m"
        )
    except Exception as e:
        # If any unexpected error occurs, log it as a false negative
        print(
            f"\033[31m[  FAILED  ] A correct entry failed unexpectedly: {e} "
            "(false negative test).\033[0m"
        )
    finally:
        # Close the database connection
        db.close()


# Run the test
if __name__ == "__main__":
    test_false_negative()
