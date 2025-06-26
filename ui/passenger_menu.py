from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from src.managers.passenger.profile import PassengerProfile
from src.managers.passenger.passenger_details import PassengerDetails
from src.managers.passenger.booking import PassengerBooking
from src.managers.passenger.auth import PassengerAuth
from src.managers.passenger.history import PassengerHistory
from src.managers.booking.notifications import BookingNotifier
from src.database.connection import DatabaseConnection

# Initialize managers
db_connection = DatabaseConnection()
auth_manager = PassengerAuth(db_connection)
notifier = BookingNotifier()
booking_manager = PassengerBooking(db_connection, notifier)
history_manager = PassengerHistory(db_connection)
profile_manager = PassengerProfile(db_connection)
details_manager = PassengerDetails(db_connection)

def display_passenger_menu() -> None:
    """Display the passenger management menu options."""
    print_header("Passenger Management")
    print("\n1. Register New Passenger")
    print("2. Update Passenger")
    print("3. Delete Passenger")
    print("4. Search Passengers")
    print("5. View All Passengers")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def _get_passenger_details_from_user():
    """Helper function to get new passenger details from user input."""
    print("\nCreate New Passenger Account")
    username = input("Enter username: ")
    password = input("Enter password: ")
    # In a real app, hash the password. For now, storing plaintext for simplicity.
    # from utils.helpers import hash_password
    # hashed_password = hash_password(password)
    email = input("Enter email: ")
    name = input("Enter full name: ")
    phone = input("Enter phone number: ")
    if profile_manager.create_account(username, password, email, name, phone):
        print("Registration successful!")
    else:
        print("Registration failed.")

def handle_passenger_menu() -> None:
    """Handles the passenger management menu."""
    while True:
        display_passenger_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            _get_passenger_details_from_user()
        elif choice == '2':
            # Update Passenger
            username = input("Enter username to update: ")
            field = input("Enter field to update (email, phone, name): ")
            new_value = input(f"Enter new value for {field}: ")
            profile_manager.update_profile(username, field, new_value)
        elif choice == '3':
            # Delete Passenger - Note: A safe delete would typically deactivate, not remove.
            print("Delete passenger logic not fully implemented for safety.")
            # username = input("Enter username to delete: ")
            # profile_manager.delete_account(username) # Assuming this method exists
        elif choice == '4':
            # Search Passengers
            print("Search logic not fully implemented yet.")
            # For example:
            # username = input("Enter username to search for: ")
            # profile_manager.view_profile(username)
        elif choice == '5':
            # View All Passengers
            print("Viewing all passengers is not implemented in the manager yet.")
            # This would require a `view_all_profiles` method in PassengerProfile
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")
        
        input("\nPress Enter to continue...") 