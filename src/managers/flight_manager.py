"""
Flight management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from enum import Enum
from datetime import datetime, timedelta

class FlightStatus(Enum):
    """Enum for flight statuses."""
    SCHEDULED = "SCHEDULED"
    DELAYED = "DELAYED"
    CANCELLED = "CANCELLED"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"

class FlightManager:
    """Handles all flight-related operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def add_flight(self, flight_series: str, flight_number: int, departure: str, 
                  arrival: str, departure_time: str, arrival_time: str, 
                  total_seats: int, available_seats: int) -> None:
        """Add a new flight to the system."""
        query = """INSERT INTO flight (flightseries, flightnumber, departure, arrival, 
                  departuretime, arrivaltime, totalseats, available, status) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (flight_series, flight_number, departure, arrival, 
                 departure_time, arrival_time, total_seats, available_seats, 
                 FlightStatus.SCHEDULED.value)
        self.db.execute_query(query, params)
        print("Flight added successfully")

    def update_flight_status(self, flight_series: str, flight_number: int, 
                           new_status: str, delay_minutes: int = None) -> None:
        """Update the status of a flight with optional delay information."""
        try:
            # Validate the status
            status = FlightStatus(new_status.upper())
            
            # Get current flight details
            query = "SELECT departuretime, arrivaltime FROM flight WHERE flightseries = %s AND flightnumber = %s"
            result = self.db.execute_query(query, (flight_series, flight_number))
            
            if not result:
                print("Flight not found")
                return
                
            current_departure = result[0][0]
            current_arrival = result[0][1]
            
            # If delayed, update the times
            if status == FlightStatus.DELAYED and delay_minutes:
                new_departure = current_departure + timedelta(minutes=delay_minutes)
                new_arrival = current_arrival + timedelta(minutes=delay_minutes)
                query = """UPDATE flight 
                          SET status = %s, departuretime = %s, arrivaltime = %s 
                          WHERE flightseries = %s AND flightnumber = %s"""
                self.db.execute_query(query, (status.value, new_departure, new_arrival, 
                                           flight_series, flight_number))
                print(f"Flight delayed by {delay_minutes} minutes")
            else:
                query = "UPDATE flight SET status = %s WHERE flightseries = %s AND flightnumber = %s"
                self.db.execute_query(query, (status.value, flight_series, flight_number))
                print(f"Flight status updated to {status.value}")
                
        except ValueError:
            print(f"Invalid status. Valid statuses are: {', '.join([s.value for s in FlightStatus])}")

    def get_flight_status(self, flight_series: str, flight_number: int) -> str:
        """Get the current status of a flight."""
        query = "SELECT status FROM flight WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        if result:
            return result[0][0]
        return None

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