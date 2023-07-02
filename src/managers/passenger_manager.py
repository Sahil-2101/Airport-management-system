"""
Passenger management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from .passenger import PassengerDetails, PassengerCancellation

class PassengerManager:
    """Handles all passenger operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.details = PassengerDetails(db)
        self.cancellation = PassengerCancellation(db)

    def check_details(self, passport_ser: str, passport_no: int) -> None:
        """Display passenger details."""
        self.details.check_details(passport_ser, passport_no)

    def cancel_flight(self, passport_ser: str, passport_no: int) -> None:
        """Cancel a passenger's flight booking."""
        self.cancellation.cancel_flight(passport_ser, passport_no) 