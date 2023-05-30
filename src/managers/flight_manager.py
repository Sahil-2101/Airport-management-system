"""
Flight management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class FlightManager:
    """Handles all flight-related operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def add_flight(self, flight_series: str, flight_number: int, departure: str, 
                  arrival: str, departure_time: str, arrival_time: str, 
                  total_seats: int, available_seats: int, status: str) -> None:
        """Add a new flight to the system."""
        query = """INSERT INTO flight (flightseries, flightnumber, departure, arrival, 
                  departuretime, arrivaltime, totalseats, available, status) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (flight_series, flight_number, departure, arrival, 
                 departure_time, arrival_time, total_seats, available_seats, status)
        self.db.execute_query(query, params)
        print("Flight added successfully")

    def update_flight_status(self, flight_series: str, flight_number: int, new_status: str) -> None:
        """Update the status of a flight (e.g., On Time, Delayed, Cancelled)."""
        query = "UPDATE flight SET status = %s WHERE flightseries = %s AND flightnumber = %s"
        self.db.execute_query(query, (new_status, flight_series, flight_number))
        print("Flight status updated successfully")

    def view_flight_schedule(self, date: str = None) -> None:
        """View flight schedule for a specific date or all flights."""
        if date:
            query = """SELECT * FROM flight 
                      WHERE DATE(departuretime) = %s 
                      ORDER BY departuretime"""
            result = self.db.execute_query(query, (date,))
        else:
            query = "SELECT * FROM flight ORDER BY departuretime"
            result = self.db.execute_query(query)

        if result:
            print("\nFlight Schedule:")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}")
        else:
            print("No flights found")

    def search_flights(self, departure: str = None, arrival: str = None) -> None:
        """Search for flights based on departure and/or arrival locations."""
        if departure and arrival:
            query = "SELECT * FROM flight WHERE departure = %s AND arrival = %s"
            params = (departure, arrival)
        elif departure:
            query = "SELECT * FROM flight WHERE departure = %s"
            params = (departure,)
        elif arrival:
            query = "SELECT * FROM flight WHERE arrival = %s"
            params = (arrival,)
        else:
            print("Please specify at least one search criteria")
            return

        result = self.db.execute_query(query, params)
        if result:
            print("\nSearch Results:")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}")
        else:
            print("No flights found matching the criteria") 