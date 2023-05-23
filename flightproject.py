"""
Airport Management System
A comprehensive system for managing airport operations including flight bookings,
passenger management, and employee administration.

@author Sahil Khatri
"""

import mysql.connector as ms
from typing import List, Tuple, Optional
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "1234",
    "database": "flightproject"
}

class DatabaseConnection:
    """Handles database connection and cursor operations."""
    
    def __init__(self):
        """Initialize database connection and cursor."""
        try:
            self.connection = ms.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to database")
            self.cursor = self.connection.cursor()
        except ms.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: tuple = None) -> Optional[List]:
        """Execute a database query and return results."""
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                return self.cursor.fetchall()
            self.connection.commit()
            return None
        except ms.Error as e:
            print(f"Error executing query: {e}")
            return None

class AdminManager:
    """Handles all administrative operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def display_employee(self, emp_id: int) -> None:
        """Display details of a specific employee."""
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            for row in result:
                print(row)

    def insert_employee(self, emp_id: int, name: str, sales: int, job_id: int) -> None:
        """Insert a new employee record."""
        query = "INSERT INTO Employee VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (emp_id, name, sales, job_id))

    def update_employee(self, emp_id: int, field: str, new_value: str) -> None:
        """Update specific field of an employee record."""
        query = f"UPDATE Employee SET {field} = %s WHERE employeeid = %s"
        self.db.execute_query(query, (new_value, emp_id))

    def delete_employee(self, emp_id: int) -> None:
        """Delete an employee record after confirmation."""
        # First display the record
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            print(f"Employee details to be deleted: {result[0]}")
            if input("Confirm deletion? (yes/no): ").lower() == 'yes':
                query = "DELETE FROM Employee WHERE employeeid = %s"
                self.db.execute_query(query, (emp_id,))
                print("Record deleted successfully")

class EmployeeManager:
    """Handles all employee operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def display_flight(self, flight_series: str, flight_number: int) -> None:
        """Display details of a specific flight."""
        query = "SELECT * FROM flight WHERE flightseries = %s AND flightnumber = %s"
        result = self.db.execute_query(query, (flight_series, flight_number))
        if result:
            for row in result:
                print(row)

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

class PassengerManager:
    """Handles all passenger operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def check_details(self, passport_ser: str, passport_no: int) -> None:
        """Display passenger details."""
        query = "SELECT * FROM passenger WHERE passportserial = %s AND passportnumber = %s"
        result = self.db.execute_query(query, (passport_ser, passport_no))
        if result:
            for row in result:
                print(row)

    def cancel_flight(self, passport_ser: str, passport_no: int) -> None:
        """Cancel a passenger's flight booking."""
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

def main():
    """Main function to run the airport management system."""
    try:
        # Initialize database connection
        db = DatabaseConnection()
        
        # Initialize managers
        admin_manager = AdminManager(db)
        employee_manager = EmployeeManager(db)
        passenger_manager = PassengerManager(db)
        flight_manager = FlightManager(db)

        while True:
            print("\nWelcome to Airport Management System")
            print("1. Admin")
            print("2. Employee")
            print("3. Passenger")
            print("4. Flight Management")
            print("5. Exit")
            
            choice = int(input("Enter your option: "))
            
            if choice == 5:
                print("Thank you for using the system!")
                break
                
            if choice == 1:
                password = int(input("Enter admin password: "))
                # Verify admin password
                query = "SELECT * FROM admin WHERE password = %s"
                result = db.execute_query(query, (password,))
                if result:
                    print(f"Welcome {result[0][0]}")
                    while True:
                        print("\nAdmin Menu:")
                        print("1. Display Employee")
                        print("2. Insert Employee")
                        print("3. Update Employee")
                        print("4. Delete Employee")
                        print("5. Back to Main Menu")
                        
                        admin_choice = int(input("Enter your option: "))
                        if admin_choice == 5:
                            break
                            
                        if admin_choice == 1:
                            emp_id = int(input("Enter employee ID: "))
                            admin_manager.display_employee(emp_id)
                        elif admin_choice == 2:
                            emp_id = int(input("Enter employee ID: "))
                            name = input("Enter name: ")
                            sales = int(input("Enter sales: "))
                            job_id = int(input("Enter job ID: "))
                            admin_manager.insert_employee(emp_id, name, sales, job_id)
                        elif admin_choice == 3:
                            emp_id = int(input("Enter employee ID: "))
                            field = input("Enter field to update: ")
                            new_value = input("Enter new value: ")
                            admin_manager.update_employee(emp_id, field, new_value)
                        elif admin_choice == 4:
                            emp_id = int(input("Enter employee ID: "))
                            admin_manager.delete_employee(emp_id)
                else:
                    print("Incorrect password")
                    
            elif choice == 2:
                password = int(input("Enter employee password: "))
                # Verify employee password
                query = "SELECT * FROM employeepass WHERE password = %s"
                result = db.execute_query(query, (password,))
                if result:
                    print(f"Welcome {result[0][0]}")
                    while True:
                        print("\nEmployee Menu:")
                        print("1. Display Flight")
                        print("2. Book Flight")
                        print("3. Back to Main Menu")
                        
                        emp_choice = int(input("Enter your option: "))
                        if emp_choice == 3:
                            break
                            
                        if emp_choice == 1:
                            flight_series = input("Enter flight series: ")
                            flight_number = int(input("Enter flight number: "))
                            employee_manager.display_flight(flight_series, flight_number)
                        elif emp_choice == 2:
                            flight_series = input("Enter flight series: ")
                            flight_number = int(input("Enter flight number: "))
                            num_passengers = int(input("Enter number of passengers: "))
                            employee_manager.book_flight(flight_series, flight_number, num_passengers)
                else:
                    print("Incorrect password")
                    
            elif choice == 3:
                while True:
                    print("\nPassenger Menu:")
                    print("1. Check Details")
                    print("2. Cancel Flight")
                    print("3. Back to Main Menu")
                    
                    pass_choice = int(input("Enter your option: "))
                    if pass_choice == 3:
                        break
                        
                    if pass_choice == 1:
                        passport_ser = input("Enter passport serial: ")
                        passport_no = int(input("Enter passport number: "))
                        passenger_manager.check_details(passport_ser, passport_no)
                    elif pass_choice == 2:
                        passport_ser = input("Enter passport serial: ")
                        passport_no = int(input("Enter passport number: "))
                        passenger_manager.cancel_flight(passport_ser, passport_no)

            elif choice == 4:
                while True:
                    print("\nFlight Management Menu:")
                    print("1. Add New Flight")
                    print("2. Update Flight Status")
                    print("3. View Flight Schedule")
                    print("4. Search Flights")
                    print("5. Back to Main Menu")
                    
                    flight_choice = int(input("Enter your option: "))
                    if flight_choice == 5:
                        break
                        
                    if flight_choice == 1:
                        flight_series = input("Enter flight series: ")
                        flight_number = int(input("Enter flight number: "))
                        departure = input("Enter departure location: ")
                        arrival = input("Enter arrival location: ")
                        departure_time = input("Enter departure time (YYYY-MM-DD HH:MM): ")
                        arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
                        total_seats = int(input("Enter total seats: "))
                        available_seats = int(input("Enter available seats: "))
                        status = input("Enter flight status: ")
                        flight_manager.add_flight(flight_series, flight_number, departure, 
                                               arrival, departure_time, arrival_time,
                                               total_seats, available_seats, status)
                    elif flight_choice == 2:
                        flight_series = input("Enter flight series: ")
                        flight_number = int(input("Enter flight number: "))
                        new_status = input("Enter new status: ")
                        flight_manager.update_flight_status(flight_series, flight_number, new_status)
                    elif flight_choice == 3:
                        date = input("Enter date to view schedule (YYYY-MM-DD) or press Enter for all: ")
                        flight_manager.view_flight_schedule(date if date else None)
                    elif flight_choice == 4:
                        departure = input("Enter departure location (optional): ")
                        arrival = input("Enter arrival location (optional): ")
                        flight_manager.search_flights(departure, arrival)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db' in locals():
            db.connection.close()

if __name__ == "__main__":
    main() 