from sales_rep import SalesRep
from database import Database

# Initialize the database and SalesRep instance
db = Database()
sr = SalesRep(db)


def test_add_sales_rep_invalid_name():
    try:
        sr.add_sales_rep("")  # Attempt to add an empty name
        print(
            "\033[31m[  FAILED  ] Empty name was accepted "
            "(unexpected pass).\033[0m"
        )
    except Exception:
        print(
            "\033[31m[  FAILED  ] Empty name rejected as expected "
            "(true negative test for add_sales_rep).\033[0m"
        )


def test_get_all_sales_reps_empty_db():
    # Attempt to retrieve sales reps from an empty database
    reps = sr.get_all_sales_reps()
    if not reps:
        print(
            "\033[31m[  FAILED  ] No sales reps found as expected "
            "(true negative test for get_all_sales_reps).\033[0m"
        )
    else:
        print(
            "\033[31m[  FAILED  ] Unexpected entries found "
            "(unexpected pass).\033[0m"
        )


def test_select_nonexistent_sales_rep():
    # Attempt to select a non-existent ID (ID 999 is arbitrary and should not exist)
    rep = sr.select_sales_rep_by_id(999)
    if rep is None:
        print(
            "\033[31m[  FAILED  ] Non-existent rep selection handled "
            "as expected (true negative test for select_sales_rep_by_id).\033[0m"
        )
    else:
        print(
            "\033[31m[  FAILED  ] Unexpected rep found "
            "(unexpected pass).\033[0m"
        )


def test_duplicate_sales_rep():
    # Add a sales rep with a unique name (should succeed)
    sr.add_sales_rep("Duplicate")
    try:
        # Attempt to add the same name again (should fail)
        sr.add_sales_rep("Duplicate")
        print(
            "\033[31m[  FAILED  ] Duplicate entry was accepted "
            "(unexpected pass).\033[0m"
        )
    except Exception:
        print(
            "\033[31m[  FAILED  ] Duplicate entry error detected "
            "as expected (true negative test for duplicate sales rep).\033[0m"
        )


def test_invalid_unique_sales_rep_name():
    try:
        # Attempt to add a sales rep with an invalid name, e.g., "A" (if invalid)
        sr.add_sales_rep("A")
        print(
            "\033[31m[  FAILED  ] Invalid unique name was accepted "
            "(unexpected pass).\033[0m"
        )
    except Exception:
        print(
            "\033[31m[  FAILED  ] Invalid name rejected as expected "
            "(true negative test for unique sales rep).\033[0m"
        )


# Run all tests
print("Starting true negative tests...")
test_add_sales_rep_invalid_name()
test_get_all_sales_reps_empty_db()
test_select_nonexistent_sales_rep()
test_duplicate_sales_rep()
test_invalid_unique_sales_rep_name()

# Close the database connection
db.close()
