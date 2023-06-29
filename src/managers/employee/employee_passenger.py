"""
Employee passenger operations module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class EmployeePassenger:
    """Handles employee passenger-related operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def book_flight(self, flight_series: str, flight_number: int, num_passengers: int) -> None:
        """Book flight tickets for passengers."""
        # Check seat availability
        query = "SELECT available FROM flight WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        
        if result and result[0][0] >= num_passengers:
            print("Please enter passenger details:")
            for _ in range(num_passengers):
                self._get_passenger_details(flight_series, flight_number)
            
            # Update available seats
            query = "UPDATE flight SET available = available - %s WHERE flightseries = %s AND flightnumber = %s"
            self.db.execute_query(query, (num_passengers, flight_series, flight_number))
        else:
            print("Not enough seats available")

    def _get_passenger_details(self, flight_series: str, flight_number: int) -> None:
        """Helper method to collect and store passenger details."""
        name = input("Enter name: ")
        passport_ser = input("Enter passport serial alphabet: ")
        passport_no = int(input("Enter passport number: "))
        dob = input("Enter date of birth: ")
        passport_doi = input("Enter passport date of issue: ")
        passport_doe = input("Enter passport date of expiry: ")
        visa_no = int(input("Enter visa number: "))

        query = """INSERT INTO passenger VALUES 
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (flight_series, flight_number, name, passport_ser, passport_no,
                 dob, passport_doi, passport_doe, visa_no)
        self.db.execute_query(query, params)

    def update_passenger_details(self, passport_ser: str, passport_no: int, field: str, new_value: str) -> None:
        """Update specific passenger details."""
        query = f"UPDATE passenger SET {field} = %s WHERE passport_serial = %s AND passport_number = %s"
        self.db.execute_query(query, (new_value, passport_ser, passport_no))
        print(f"Passenger details updated successfully.") 