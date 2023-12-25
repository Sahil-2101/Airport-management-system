"""
Flight schedule management module for the Airport Management System.
"""

from datetime import timedelta
from src.database.connection import DatabaseConnection

class FlightSchedule:
    """Handles flight schedule operations."""
    
    def __init__(self):
        """Initialize the flight schedule manager."""
        self.db = DatabaseConnection()

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
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)\tStops\tFare($)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}\t{row[11]}\t{row[12]}")
        else:
            print("No flights found")

    def reschedule_flight(self, flight_series: str, flight_number: int, new_departure_time: str, new_arrival_time: str) -> None:
        """Reschedule a flight by updating its departure and arrival times."""
        query = "UPDATE flight SET departuretime = %s, arrivaltime = %s WHERE flightseries = %s AND flightnumber = %s"
        self.db.execute_query(query, (new_departure_time, new_arrival_time, flight_series, flight_number))
        print(f"Flight {flight_series}{flight_number} rescheduled to depart at {new_departure_time} and arrive at {new_arrival_time}.") 