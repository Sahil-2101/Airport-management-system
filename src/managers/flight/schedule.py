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

    def add_flight(self) -> None:
        """Add a new flight to the system."""
        print("\nAdd New Flight")
        print("-" * 50)
        
        # Get flight details
        flight_series = input("Enter flight series (e.g., AA): ").upper()
        flight_number = input("Enter flight number: ")
        departure = input("Enter departure airport code: ").upper()
        arrival = input("Enter arrival airport code: ").upper()
        departure_time = input("Enter departure time (YYYY-MM-DD HH:MM): ")
        arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
        available_seats = input("Enter number of available seats: ")
        status = "Scheduled"  # Default status for new flights
        distance = input("Enter distance in kilometers: ")
        duration = input("Enter duration in minutes: ")
        stops = input("Enter number of stops: ")
        fare = input("Enter base fare: ")
        
        try:
            query = """
                INSERT INTO flights (
                    flight_series, flight_number, departure, arrival,
                    departure_time, arrival_time, available_seats,
                    status, distance, duration, stops, fare
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                flight_series, flight_number, departure, arrival,
                departure_time, arrival_time, available_seats,
                status, distance, duration, stops, fare
            )
            self.db.execute_query(query, params)
            print("\nFlight added successfully!")
            
        except Exception as e:
            print(f"\nError adding flight: {str(e)}")

    def update_flight(self) -> None:
        """Update an existing flight's details."""
        print("\nUpdate Flight")
        print("-" * 50)
        
        flight_series = input("Enter flight series: ").upper()
        flight_number = input("Enter flight number: ")
        
        # Get updated details
        departure = input("Enter new departure airport code (press Enter to skip): ").upper()
        arrival = input("Enter new arrival airport code (press Enter to skip): ").upper()
        departure_time = input("Enter new departure time (press Enter to skip): ")
        arrival_time = input("Enter new arrival time (press Enter to skip): ")
        available_seats = input("Enter new number of available seats (press Enter to skip): ")
        status = input("Enter new status (press Enter to skip): ")
        distance = input("Enter new distance in kilometers (press Enter to skip): ")
        duration = input("Enter new duration in minutes (press Enter to skip): ")
        stops = input("Enter new number of stops (press Enter to skip): ")
        fare = input("Enter new base fare (press Enter to skip): ")
        
        try:
            updates = []
            params = []
            
            if departure:
                updates.append("departure = %s")
                params.append(departure)
            if arrival:
                updates.append("arrival = %s")
                params.append(arrival)
            if departure_time:
                updates.append("departure_time = %s")
                params.append(departure_time)
            if arrival_time:
                updates.append("arrival_time = %s")
                params.append(arrival_time)
            if available_seats:
                updates.append("available_seats = %s")
                params.append(available_seats)
            if status:
                updates.append("status = %s")
                params.append(status)
            if distance:
                updates.append("distance = %s")
                params.append(distance)
            if duration:
                updates.append("duration = %s")
                params.append(duration)
            if stops:
                updates.append("stops = %s")
                params.append(stops)
            if fare:
                updates.append("fare = %s")
                params.append(fare)
            
            if updates:
                query = f"""
                    UPDATE flights 
                    SET {', '.join(updates)}
                    WHERE flight_series = %s AND flight_number = %s
                """
                params.extend([flight_series, flight_number])
                self.db.execute_query(query, tuple(params))
                print("\nFlight updated successfully!")
            else:
                print("\nNo updates provided.")
                
        except Exception as e:
            print(f"\nError updating flight: {str(e)}")

    def delete_flight(self) -> None:
        """Delete a flight from the system."""
        print("\nDelete Flight")
        print("-" * 50)
        
        flight_series = input("Enter flight series: ").upper()
        flight_number = input("Enter flight number: ")
        confirm = input("Are you sure you want to delete this flight? (y/n): ")
        
        if confirm.lower() == 'y':
            try:
                query = "DELETE FROM flights WHERE flight_series = %s AND flight_number = %s"
                self.db.execute_query(query, (flight_series, flight_number))
                print("\nFlight deleted successfully!")
                
            except Exception as e:
                print(f"\nError deleting flight: {str(e)}")
        else:
            print("\nDeletion cancelled.")

    def view_flight_schedule(self, date: str = None) -> None:
        """View flight schedule for a specific date or all flights."""
        if date:
            query = """SELECT * FROM flights 
                      WHERE DATE(departure_time) = %s 
                      ORDER BY departure_time"""
            result = self.db.execute_query(query, (date,))
        else:
            query = "SELECT * FROM flights ORDER BY departure_time"
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
        query = "UPDATE flights SET departure_time = %s, arrival_time = %s WHERE flight_series = %s AND flight_number = %s"
        self.db.execute_query(query, (new_departure_time, new_arrival_time, flight_series, flight_number))
        print(f"Flight {flight_series}{flight_number} rescheduled to depart at {new_departure_time} and arrive at {new_arrival_time}.") 