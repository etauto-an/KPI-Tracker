# KPI Tracker

KPI Tracker is a Python-based project for managing and tracking key performance indicators (KPIs) for sales representatives. It utilizes a SQLite database to store data and provides a command-line and web interface for managing sales reps and calculating various performance metrics.

## Features

- **Sales Rep Management**: Add, list, and manage sales representatives.
- **KPI Calculation**: Calculate performance metrics (show %, offer %, close %, cash per call, revenue per call) for individual reps or compare across the team.
- **Modular Design**: Separate modules for database, sales rep management, and KPI calculations.
- **Testing**: Automated testing with a Makefile, covering various scenarios, including false positives and negatives.
- **CLI and Web Interface**: Command-line options and a Flask-based web UI (optional).


## Installation

### Prerequisites

- Python 3.x
- [Flask](https://flask.palletsprojects.com/) (if using the web UI)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/KPI-Tracker.git
   cd KPI-Tracker

2. **Set up a virtual environment (recommended):**

  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

