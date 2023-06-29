"""
Employee flight operations module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class EmployeeFlight:
    """Handles employee flight-related operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def display_flight(self, flight_series: str, flight_number: int) -> None:
        """Display details of a specific flight."""
        query = "SELECT * FROM flight WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        if result:
            for row in result:
                print(row)

    def view_assigned_flights(self, emp_id: int) -> None:
        """View flights assigned to a specific employee."""
        query = "SELECT * FROM flight WHERE assigned_employee_id = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            print("\nAssigned Flights:")
            for row in result:
                print(f"Flight: {row[0]}{row[1]}, From: {row[2]}, To: {row[3]}, Departure: {row[4]}, Arrival: {row[5]}, Status: {row[8]}")
        else:
            print("No flights assigned to this employee.") 