"""
Flight management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from src.managers.flight.status import FlightStatus
from src.managers.flight.fare import FareCalculator
from src.managers.flight.search import FlightSearch
from src.managers.flight.schedule import FlightSchedule
from datetime import datetime, timedelta

class FlightManager:
    """Handles all flight-related operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.search = FlightSearch(db)
        self.schedule = FlightSchedule(db)

    def add_flight(self, flight_series: str, flight_number: int, departure: str, 
                  arrival: str, departure_time: str, arrival_time: str, 
                  total_seats: int, available_seats: int, distance: float, duration: int, stops: int) -> None:
        """Add a new flight to the system."""
        fare = FareCalculator.calculate_fare(distance, duration, stops)
        query = """INSERT INTO flight (flightseries, flightnumber, departure, arrival, 
                  departuretime, arrivaltime, totalseats, available, status, distance, duration, stops, fare) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (flight_series, flight_number, departure, arrival, 
                 departure_time, arrival_time, total_seats, available_seats, 
                 FlightStatus.SCHEDULED.value, distance, duration, stops, fare)
        self.db.execute_query(query, params)
        print("Flight added successfully")

    def update_flight_status(self, flight_number, new_status, delay_minutes=None):
        """Update the status of a flight"""
        try:
            if new_status not in [status.value for status in FlightStatus]:
                raise ValueError(f"Invalid status. Must be one of: {[status.value for status in FlightStatus]}")

            if new_status == FlightStatus.DELAYED.value and delay_minutes is not None:
                self.cursor.execute("""
                    SELECT departuretime, arrivaltime 
                    FROM flight 
                    WHERE flightnumber = %s
                """, (flight_number,))
                result = self.cursor.fetchone()
                if not result:
                    raise ValueError(f"Flight {flight_number} not found")
                
                delay_minutes = int(delay_minutes)
                departure_time = result[0] + timedelta(minutes=delay_minutes)
                arrival_time = result[1] + timedelta(minutes=delay_minutes)
                
                self.cursor.execute("""
                    UPDATE flight 
                    SET status = %s, departuretime = %s, arrivaltime = %s
                    WHERE flightnumber = %s
                """, (new_status, departure_time, arrival_time, flight_number))
            else:
                self.cursor.execute("""
                    UPDATE flight 
                    SET status = %s
                    WHERE flightnumber = %s
                """, (new_status, flight_number))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating flight status: {str(e)}")
            return False

    def get_flight_status(self, flight_series: str, flight_number: int) -> str:
        """Get the current status of a flight."""
        query = "SELECT status FROM flight WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        if result:
            return result[0][0]
        return None

    # Delegate to specialized classes
    def view_flight_schedule(self, date: str = None) -> None:
        """View flight schedule for a specific date or all flights."""
        self.schedule.view_flight_schedule(date)

    def search_flights(self, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights based on departure and/or arrival locations."""
        self.search.search_flights(departure, arrival, page, page_size)

    def search_flights_advanced(self, date: str = None, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights by date, departure, and/or arrival locations."""
        self.search.search_flights_advanced(date, departure, arrival, page, page_size)

    def reschedule_flight(self, flight_series: str, flight_number: int, new_departure_time: str, new_arrival_time: str) -> None:
        """Reschedule a flight by updating its departure and arrival times."""
        self.schedule.reschedule_flight(flight_series, flight_number, new_departure_time, new_arrival_time) 