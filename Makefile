# Makefile with enhanced test output styling, hidden commands, and
# automatic cleaning

# Python interpreter (if using a virtual environment, replace with its path)
PYTHON := python3
PYTHONPATH := PYTHONPATH=.

# Colors for output
GREEN := "\033[32m"
ORANGE := "\033[33m"
RED := "\033[31m"
CYAN := "\033[36m"
RESET := "\033[0m"

# Default target: runs all tests
.PHONY: all
all: test_add_sales_rep test_get_all_sales_reps test_select_sales_rep \
    test_false_positive test_false_negative test_true_negative \
    test_kpi_calculator

# Code formatter using black
format:
	@echo $(CYAN)"Running black to format all Python files..."$(RESET)
	@black --line-length 80 .  # Format all .py files in current directory
	@echo $(GREEN)"Formatting complete."$(RESET)

# Clean up the database before tests
clean:
	@rm -f kpi_tracker_v2.db
	@echo "==============================="
	@echo $(CYAN)"Database cleaned."$(RESET)
	@echo "==============================="

# Initialize the database (creates tables)
init: clean
	@echo "==============================="
	@$(PYTHONPATH) $(PYTHON) -c \
	    "from database import Database; db = Database(); db.close()"
	@echo $(CYAN)"Database initialized."$(RESET)
	@echo "==============================="

# Test: Add a new sales rep
test_add_sales_rep: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_add_sales_rep"$(RESET)
	@$(PYTHONPATH) $(PYTHON) -c \
	    "from sales_rep import SalesRep; from database import Database; \
db = Database(); \
sr = SalesRep(db); \
sr.add_sales_rep('John Doe'); \
db.close()"
	@echo $(GREEN)"[       OK ] test_add_sales_rep completed successfully"$(RESET)
	@echo "==============================="

# Test: Get all sales reps
test_get_all_sales_reps: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_get_all_sales_reps"$(RESET)
	@$(PYTHONPATH) $(PYTHON) -c \
	    "from sales_rep import SalesRep; from database import Database; \
db = Database(); \
sr = SalesRep(db); \
sr.add_sales_rep('Jane Smith'); \
print(sr.get_all_sales_reps()); \
db.close()"
	@echo $(GREEN)"[       OK ] test_get_all_sales_reps completed successfully"$(RESET)
	@echo "==============================="

# Test: Select a sales rep by ID
test_select_sales_rep: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_select_sales_rep"$(RESET)
	@$(PYTHONPATH) $(PYTHON) -c \
	    "from sales_rep import SalesRep; from database import Database; \
db = Database(); \
sr = SalesRep(db); \
sr.add_sales_rep('Alice Johnson'); \
rep = sr.select_sales_rep_by_id(1); \
print(rep); \
db.close()"
	@echo $(GREEN)"[       OK ] test_select_sales_rep completed successfully"$(RESET)
	@echo "==============================="

# False Positive Test: Adding a duplicate sales rep should fail
test_false_positive: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_false_positive"$(RESET)
	@$(PYTHONPATH) $(PYTHON) tests/test_false_positive.py
	@echo $(GREEN)"[       OK ] test_false_positive completed successfully"$(RESET)
	@echo "==============================="

# False Negative Test: Adding unique sales reps should pass but will simulate failure
test_false_negative: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_false_negative"$(RESET)
	@$(PYTHONPATH) $(PYTHON) tests/test_false_negative.py
	@echo $(GREEN)"[       OK ] test_false_negative completed successfully"$(RESET)
	@echo "==============================="

# True Negative Test: Run all true negative tests in one script
test_true_negative: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting all true negative tests"$(RESET)
	@$(PYTHONPATH) $(PYTHON) tests/test_true_negative.py
	@echo $(GREEN)"[       OK ] All true negative tests completed successfully"$(RESET)
	@echo "==============================="

# Test for KPI Calculator functionality
test_kpi_calculator: init
	@echo "==============================="
	@echo $(ORANGE)"[ RUN      ] Starting test_kpi_calculator"$(RESET)
	@$(PYTHONPATH) $(PYTHON) tests/test_kpi_calculator.py
	@echo $(GREEN)"[       OK ] test_kpi_calculator completed successfully"$(RESET)
	@echo "==============================="
