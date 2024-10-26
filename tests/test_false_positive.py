from sales_rep import SalesRep
from database import Database

# Initialize the database and SalesRep instance
db = Database()
sr = SalesRep(db)

# Add a unique name (should succeed)
sr.add_sales_rep("Duplicate")

try:
    # Attempt to add the same name again (should fail)
    sr.add_sales_rep("Duplicate")
    print(
        "\033[31m[  FAILED  ] Duplicate entry was accepted "
        "(simulated false positive).\033[0m"
    )
except Exception:
    print(
        "\033[31m[  FAILED  ] Duplicate entry error detected as expected "
        "(true negative test).\033[0m"
    )

# Close the database connection
db.close()
