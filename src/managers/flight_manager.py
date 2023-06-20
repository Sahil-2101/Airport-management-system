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
        self.last_searched_route = None  # Store the last searched route

    def add_flight(self, flight_series: str, flight_number: int, departure: str, 
                  arrival: str, departure_time: str, arrival_time: str, 
                  total_seats: int, available_seats: int, distance: float, duration: int) -> None:
        """Add a new flight to the system, including distance and duration."""
        query = """INSERT INTO flight (flightseries, flightnumber, departure, arrival, 
                  departuretime, arrivaltime, totalseats, available, status, distance, duration) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (flight_series, flight_number, departure, arrival, 
                 departure_time, arrival_time, total_seats, available_seats, 
                 FlightStatus.SCHEDULED.value, distance, duration)
        self.db.execute_query(query, params)
        print("Flight added successfully")

    def update_flight_status(self, flight_number, new_status, delay_minutes=None):
        """Update the status of a flight"""
        try:
            # Validate the new status
            if new_status not in [status.value for status in FlightStatus]:
                raise ValueError(f"Invalid status. Must be one of: {[status.value for status in FlightStatus]}")

            # If status is DELAYED, update departure and arrival times
            if new_status == FlightStatus.DELAYED.value and delay_minutes is not None:
                # Get current flight times
                self.cursor.execute("""
                    SELECT departuretime, arrivaltime 
                    FROM flight 
                    WHERE flightnumber = %s
                """, (flight_number,))
                result = self.cursor.fetchone()
                if not result:
                    raise ValueError(f"Flight {flight_number} not found")
                
                # FIX: Convert delay_minutes to int
                delay_minutes = int(delay_minutes)
                departure_time = result[0] + timedelta(minutes=delay_minutes)
                arrival_time = result[1] + timedelta(minutes=delay_minutes)
                
                # Update flight status and times
                self.cursor.execute("""
                    UPDATE flight 
                    SET status = %s, departuretime = %s, arrivaltime = %s
                    WHERE flightnumber = %s
                """, (new_status, departure_time, arrival_time, flight_number))
            else:
                # Update only the status
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

    def view_flight_schedule(self, date: str = None) -> None:
        """View flight schedule for a specific date or all flights, including distance and duration."""
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
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}")
        else:
            print("No flights found")

    def search_flights(self, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights based on departure and/or arrival locations with pagination, including distance and duration."""
        offset = (page - 1) * page_size
        if departure and arrival:
            query = "SELECT * FROM flight WHERE departure = %s AND arrival = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (departure, arrival, page_size, offset)
        elif departure:
            query = "SELECT * FROM flight WHERE departure = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (departure, page_size, offset)
        elif arrival:
            query = "SELECT * FROM flight WHERE arrival = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (arrival, page_size, offset)
        else:
            print("Please specify at least one search criteria")
            return

        result = self.db.execute_query(query, params)
        if result:
            print(f"\nSearch Results (Page {page}):")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}")
            self.last_searched_route = {'departure': departure, 'arrival': arrival}
        else:
            print("No flights found matching the criteria")

    def search_flights_advanced(self, date: str = None, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights by date, departure, and/or arrival locations with pagination, including distance and duration."""
        offset = (page - 1) * page_size
        query = "SELECT * FROM flight WHERE 1=1"
        params = []
        if date:
            query += " AND DATE(departuretime) = %s"
            params.append(date)
        if departure:
            query += " AND departure = %s"
            params.append(departure)
        if arrival:
            query += " AND arrival = %s"
            params.append(arrival)
        query += " ORDER BY departuretime LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        result = self.db.execute_query(query, tuple(params))
        if result:
            print(f"\nSearch Results (Page {page}):")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}")
            self.last_searched_route = {'departure': departure, 'arrival': arrival}
        else:
            print("No flights found matching the criteria")

    def reschedule_flight(self, flight_series: str, flight_number: int, new_departure_time: str, new_arrival_time: str) -> None:
        """Reschedule a flight by updating its departure and arrival times."""
        query = "UPDATE flight SET departuretime = %s, arrivaltime = %s WHERE flightseries = %s AND flightnumber = %s"
        self.db.execute_query(query, (new_departure_time, new_arrival_time, flight_series, flight_number))
        print(f"Flight {flight_series}{flight_number} rescheduled to depart at {new_departure_time} and arrive at {new_arrival_time}.") 