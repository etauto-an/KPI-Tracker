# test_kpi_calculator.py
import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from kpi_calculator import KPI

# Define color codes for output
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"


class TestKPI(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.kpi = KPI(self.mock_db)

    def test_calculate_kpis_normal_data(self):
        self.mock_db.fetch_all.return_value = [(100, 80, 60, 50, 5000, 10000)]

        with StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
            self.kpi.calculate_kpis(rep_id=1, name="John Doe")
            output = buf.getvalue()

        print(f"{CYAN}Output for test_calculate_kpis_normal_data:{RESET}")
        print(output)  # Print KPI report in default color (white)

        self.assertIn("Show %: 80.00%", output)
        self.assertIn("Offer %: 75.00%", output)
        self.assertIn("Close %: 83.33%", output)
        self.assertIn("Cash per Call: $62.50", output)
        self.assertIn("Revenue per Call: $125.00", output)

    def test_calculate_kpis_zero_calls(self):
        self.mock_db.fetch_all.return_value = [(0, 0, 0, 0, 0, 0)]

        with StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
            self.kpi.calculate_kpis(rep_id=1, name="John Doe")
            output = buf.getvalue()

        print(f"{CYAN}Output for test_calculate_kpis_zero_calls:{RESET}")
        print(output)  # Print KPI report in default color (white)

        self.assertIn("Show %: 0.00%", output)
        self.assertIn("Offer %: 0.00%", output)
        self.assertIn("Close %: 0.00%", output)
        self.assertIn("Cash per Call: $0.00", output)
        self.assertIn("Revenue per Call: $0.00", output)

    def test_calculate_kpis_no_data(self):
        self.mock_db.fetch_all.return_value = [
            (None, None, None, None, None, None)
        ]

        with StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
            self.kpi.calculate_kpis(rep_id=1, name="John Doe")
            output = buf.getvalue()

        print(f"{CYAN}Output for test_calculate_kpis_no_data:{RESET}")
        print(output)  # Print "No data" message in default color (white)

        self.assertIn("No data available for John Doe.", output)

    def test_compare_all_kpis(self):
        self.mock_db.fetch_all.side_effect = [
            [(1, "Alice"), (2, "Bob")],
            [(100, 80, 60, 50, 5000, 10000)],
            [(120, 90, 70, 55, 6000, 11000)],
        ]

        with StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
            self.kpi.compare_all_kpis()
            output = buf.getvalue()

        print(f"{CYAN}Output for test_compare_all_kpis:{RESET}")
        print(output)  # Print KPI comparison in default color (white)

        self.assertIn("Alice's KPI Summary:", output)
        self.assertIn("Bob's KPI Summary:", output)

    def test_compare_all_kpis_no_reps(self):
        self.mock_db.fetch_all.return_value = []

        with StringIO() as buf, unittest.mock.patch("sys.stdout", buf):
            self.kpi.compare_all_kpis()
            output = buf.getvalue()

        print(f"{CYAN}Output for test_compare_all_kpis_no_reps:{RESET}")
        print(
            output
        )  # Print "No reps available" message in default color (white)

        self.assertIn("No sales reps available for comparison.", output)


if __name__ == "__main__":
    unittest.main()
