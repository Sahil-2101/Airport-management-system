"""
Passenger details operations module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class PassengerDetails:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def check_details(self, passport_ser: str, passport_no: int) -> None:
        query = "SELECT * FROM passenger WHERE passportserial = %s AND passportnumber = %s"
        result = self.db.execute_query(query, (passport_ser, passport_no))
        if result:
            for row in result:
                print(row) 