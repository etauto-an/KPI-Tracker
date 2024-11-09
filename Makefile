# Python interpreter (if using a virtual environment, replace with its path)
PYTHON := python3
PYTHONPATH := PYTHONPATH=.

# Colors for output
GREEN := "\033[32m"
ORANGE := "\033[33m"
RED := "\033[31m"
CYAN := "\033[36m"
RESET := "\033[0m"

# Code formatter using black
format:
	@echo $(CYAN)"Running black to format all Python files..."$(RESET)
	@black --line-length 80 .  # Format all .py files in current directory
	@echo $(GREEN)"Formatting complete."$(RESET)

# Clean up the database before tests
clean:
	@rm -f kpi_tracker_v2.db
	@echo "======================================="
	@echo $(CYAN)"Database cleaned."$(RESET)
	@echo "======================================="

# Initialize the database (creates tables)
init: clean
	@echo "======================================="
	@$(PYTHONPATH) $(PYTHON) -c "\
		from database import Database; db = Database(); db.close()"
	@echo $(CYAN)"Database initialized."$(RESET)
	@echo "======================================="

# Compile all Python files to bytecode
all:
	@echo $(CYAN)"Compiling all Python files to bytecode..."$(RESET)
	@$(PYTHON) -m compileall .
	@echo $(GREEN)"Compilation complete."$(RESET)

# Clear the __pycache__ directories and compiled .pyc files
clear_cache:
	@echo $(RED)"Clearing __pycache__ directories and .pyc files..."$(RESET)
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -type f -delete
	@echo $(GREEN)"Cache cleared."$(RESET)
