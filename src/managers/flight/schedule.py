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
        departuretime = input("Enter departure time (YYYY-MM-DD HH:MM): ")
        arrivaltime = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
        available_seats = input("Enter number of available seats: ")
        status = "Scheduled"  # Default status for new flights
        distance = input("Enter distance in kilometers: ")
        duration = input("Enter duration in minutes: ")
        stops = input("Enter number of stops: ")
        price = input("Enter base price: ")
        
        try:
            query = """
                INSERT INTO flights (
                    flightseries, flightnumber, departure, arrival,
                    departuretime, arrivaltime, totalseats,
                    available, status, distance, duration, stops, price
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                flight_series, flight_number, departure, arrival,
                departuretime, arrivaltime, available_seats,
                available_seats, status, distance, duration, stops, price
            )
            self.db.execute_query(query, params)
            print("\nFlight added successfully!")
            
        except Exception as e:
            print(f"\nError adding flight: {str(e)}")

    def update_flight(self) -> None:
        """Update an existing flight's details."""
        print("\nUpdate Flight")
        print("-" * 50)
        
        flight_series = input("Enter flight series to update: ").upper()
        flight_number = input("Enter flight number to update: ")
        
        # Get updated details
        departure = input("Enter new departure airport code (press Enter to skip): ").upper()
        arrival = input("Enter new arrival airport code (press Enter to skip): ").upper()
        departuretime = input("Enter new departure time (press Enter to skip): ")
        arrivaltime = input("Enter new arrival time (press Enter to skip): ")
        available_seats = input("Enter new number of available seats (press Enter to skip): ")
        status = input("Enter new status (press Enter to skip): ")
        duration = input("Enter new duration in minutes (press Enter to skip): ")
        stops = input("Enter new number of stops (press Enter to skip): ")
        price = input("Enter new base price (press Enter to skip): ")
        
        try:
            updates = []
            params = []
            
            if departure:
                updates.append("departure = %s")
                params.append(departure)
            if arrival:
                updates.append("arrival = %s")
                params.append(arrival)
            if departuretime:
                updates.append("departuretime = %s")
                params.append(departuretime)
            if arrivaltime:
                updates.append("arrivaltime = %s")
                params.append(arrivaltime)
            if available_seats:
                updates.append("totalseats = %s")
                params.append(available_seats)
            if status:
                updates.append("status = %s")
                params.append(status)
            if duration:
                updates.append("duration = %s")
                params.append(duration)
            if stops:
                updates.append("stops = %s")
                params.append(stops)
            if price:
                updates.append("price = %s")
                params.append(price)
            
            if updates:
                query = f"""
                    UPDATE flights 
                    SET {', '.join(updates)}
                    WHERE flightseries = %s AND flightnumber = %s
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
                query = "DELETE FROM flights WHERE flightseries = %s AND flightnumber = %s"
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
                      WHERE DATE(departuretime) = %s 
                      ORDER BY departuretime"""
            result = self.db.execute_query(query, (date,))
        else:
            query = "SELECT * FROM flights ORDER BY departuretime"
            result = self.db.execute_query(query)

        if result:
            print("\nFlight Schedule:")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)\tStops\tPrice($)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}\t{row[11]}\t{row[12]}")
        else:
            print("No flights found")

    def search_flights(self) -> None:
        """Search for flights based on various criteria."""
        print("\nSearch Flights")
        print("-" * 50)
        
        print("\nSearch by:")
        print("1. Departure Airport")
        print("2. Arrival Airport")
        print("3. Date")
        print("4. Back")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '4':
            return
            
        search_term = input("Enter search term: ")
        
        try:
            if choice == '1':
                query = "SELECT * FROM flights WHERE departure = %s"
                params = (search_term.upper(),)
            elif choice == '2':
                query = "SELECT * FROM flights WHERE arrival = %s"
                params = (search_term.upper(),)
            elif choice == '3':
                query = "SELECT * FROM flights WHERE DATE(departuretime) = %s"
                params = (search_term,)
            else:
                print("\nInvalid choice!")
                return
            
            results = self.db.execute_query(query, params)
            if results:
                print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)\tStops\tPrice($)")
                for row in results:
                    print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}\t{row[11]}\t{row[12]}")
            else:
                print("No flights found")
                
        except Exception as e:
            print(f"\nError searching flights: {str(e)}")

    def reschedule_flight(self, flight_series: str, flight_number: int, new_departure_time: str, new_arrival_time: str) -> None:
        """Reschedule a flight by updating its departure and arrival times."""
        query = "UPDATE flights SET departuretime = %s, arrivaltime = %s WHERE flightseries = %s AND flightnumber = %s"
        self.db.execute_query(query, (new_departure_time, new_arrival_time, flight_series, flight_number))
        print(f"Flight {flight_series}{flight_number} rescheduled to depart at {new_departure_time} and arrive at {new_arrival_time}.")

    def get_flight_details(self, flight_series: str, flight_number: int) -> dict:
        """Get details of a specific flight."""
        query = "SELECT * FROM flights WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        if result:
            details = {
                'flight_series': result[0][0],
                'flight_number': result[0][1],
                'departure': result[0][2],
                'arrival': result[0][3],
                'departure_time': result[0][4],
                'arrival_time': result[0][5],
                'available_seats': result[0][7],
                'status': result[0][8],
                'distance': result[0][9],
                'duration': result[0][10],
                'stops': result[0][11],
                'price': result[0][12]
            }
            return details
        return None 