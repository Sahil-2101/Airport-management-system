"""
Main application file for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from src.managers.admin_manager import AdminManager
from src.managers.employee_manager import EmployeeManager
from src.managers.passenger_manager import PassengerManager
from src.managers.flight_manager import FlightManager
from src.managers.passenger_account_manager import PassengerAccountManager
from src.managers.booking_manager import BookingManager

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
        passenger_account_manager = PassengerAccountManager(db)
        booking_manager = BookingManager(db)

        while True:
            print("\nWelcome to Airport Management System")
            print("1. Admin")
            print("2. Employee")
            print("3. Passenger")
            print("4. Flight Management")
            print("5. Passenger Account")
            print("6. Book Flight")
            print("7. Exit")
            
            choice = int(input("Enter your option: "))
            
            if choice == 7:
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

            elif choice == 5:
                while True:
                    print("\nPassenger Account Menu:")
                    print("1. Create Account")
                    print("2. Login")
                    print("3. Back to Main Menu")
                    
                    account_choice = int(input("Enter your option: "))
                    if account_choice == 3:
                        break

                    if account_choice == 1:
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        email = input("Enter email: ")
                        name = input("Enter full name: ")
                        phone = input("Enter phone number: ")
                        passenger_account_manager.create_account(username, password, email, name, phone)
                    
                    elif account_choice == 2:
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        if passenger_account_manager.login(username, password):
                            while True:
                                print("\nAccount Menu:")
                                print("1. View Profile")
                                print("2. Update Profile")
                                print("3. Change Password")
                                print("4. View Booking History")
                                print("5. Back to Account Menu")
                                
                                profile_choice = int(input("Enter your option: "))
                                if profile_choice == 5:
                                    break
                                    
                                if profile_choice == 1:
                                    passenger_account_manager.view_profile(username)
                                elif profile_choice == 2:
                                    print("\nFields available for update:")
                                    print("1. Email")
                                    print("2. Phone")
                                    print("3. Name")
                                    field_choice = int(input("Select field to update (1-3): "))
                                    field_map = {1: 'email', 2: 'phone', 3: 'name'}
                                    if field_choice in field_map:
                                        new_value = input(f"Enter new {field_map[field_choice]}: ")
                                        passenger_account_manager.update_profile(username, 
                                                                               field_map[field_choice], 
                                                                               new_value)
                                elif profile_choice == 3:
                                    current_password = input("Enter current password: ")
                                    new_password = input("Enter new password: ")
                                    passenger_account_manager.change_password(username, 
                                                                            current_password, 
                                                                            new_password)
                                elif profile_choice == 4:
                                    passenger_account_manager.view_booking_history(username)

            elif choice == 6:
                while True:
                    print("\nBooking Menu:")
                    print("1. Book a Flight")
                    print("2. View Booking")
                    print("3. Cancel Booking")
                    print("4. Back to Main Menu")
                    
                    booking_choice = int(input("Enter your option: "))
                    if booking_choice == 4:
                        break

                    if booking_choice == 1:
                        # First, search for available flights
                        departure = input("Enter departure location: ")
                        arrival = input("Enter arrival location: ")
                        flight_manager.search_flights(departure, arrival)
                        
                        # Get flight details
                        flight_series = input("Enter flight series: ")
                        flight_number = int(input("Enter flight number: "))
                        
                        # Show available seats
                        available_seats = booking_manager.get_available_seats(flight_series, flight_number)
                        if available_seats:
                            print("\nAvailable seats:", ", ".join(available_seats))
                            seat_number = input("Enter seat number: ")
                            
                            # Get payment method
                            print("\nPayment Methods:")
                            print("1. Credit Card")
                            print("2. Debit Card")
                            print("3. Net Banking")
                            payment_choice = int(input("Select payment method (1-3): "))
                            payment_methods = {1: "CREDIT_CARD", 2: "DEBIT_CARD", 3: "NET_BANKING"}
                            payment_method = payment_methods.get(payment_choice)
                            
                            if payment_method:
                                # Get passenger account
                                username = input("Enter your username: ")
                                password = input("Enter your password: ")
                                
                                if passenger_account_manager.login(username, password):
                                    booking_manager.book_flight(username, flight_series, 
                                                              flight_number, seat_number, 
                                                              payment_method)
                        else:
                            print("No seats available for this flight")

                    elif booking_choice == 2:
                        booking_id = input("Enter booking ID: ")
                        booking_manager.view_booking(booking_id)

                    elif booking_choice == 3:
                        booking_id = input("Enter booking ID: ")
                        booking_manager.cancel_booking(booking_id)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db' in locals():
            db.connection.close()

if __name__ == "__main__":
    main() 