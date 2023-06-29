"""
Employee management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from .employee import EmployeeFlight, EmployeePassenger

class EmployeeManager:
    """Handles all employee operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.flight = EmployeeFlight(db)
        self.passenger = EmployeePassenger(db)

    def display_flight(self, flight_series: str, flight_number: int) -> None:
        """Display details of a specific flight."""
        self.flight.display_flight(flight_series, flight_number)

    def book_flight(self, flight_series: str, flight_number: int, num_passengers: int) -> None:
        """Book flight tickets for passengers."""
        self.passenger.book_flight(flight_series, flight_number, num_passengers)

    def view_assigned_flights(self, emp_id: int) -> None:
        """View flights assigned to a specific employee."""
        self.flight.view_assigned_flights(emp_id)

    def update_passenger_details(self, passport_ser: str, passport_no: int, field: str, new_value: str) -> None:
        """Update specific passenger details."""
        self.passenger.update_passenger_details(passport_ser, passport_no, field, new_value) 