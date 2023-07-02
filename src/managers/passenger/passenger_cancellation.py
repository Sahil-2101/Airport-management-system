"""
Passenger cancellation operations module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class PassengerCancellation:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def cancel_flight(self, passport_ser: str, passport_no: int) -> None:
        # Get flight details
        query = "SELECT flightserial, flightnumber FROM passenger WHERE passportserial = %s AND passportnumber = %s"
        result = self.db.execute_query(query, (passport_ser, passport_no))
        
        if result:
            # Update available seats
            query = "UPDATE flight SET available = available + 1 WHERE flightseries = %s AND flightnumber = %s"
            self.db.execute_query(query, (result[0][0], result[0][1]))
            
            # Delete passenger record
            query = "DELETE FROM passenger WHERE passportserial = %s AND passportnumber = %s"
            self.db.execute_query(query, (passport_ser, passport_no))
            print("Flight cancelled successfully") 