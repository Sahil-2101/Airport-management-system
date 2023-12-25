from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from src.managers.passenger.profile import PassengerProfile
from src.managers.passenger.passenger_details import PassengerDetails
from src.managers.passenger.booking import PassengerBooking

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

def handle_passenger_menu() -> None:
    """Handle passenger management menu selection."""
    profile_manager = PassengerProfile()
    details_manager = PassengerDetails()
    booking_manager = PassengerBooking()
    
    while True:
        clear_screen()
        display_passenger_menu()
        choice = get_valid_input(
            "Enter your choice (1-6): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5', '6']
        )
        
        if choice == '6':
            break
            
        menu_handlers: Dict[str, Callable] = {
            '1': profile_manager.register_passenger,
            '2': profile_manager.update_passenger,
            '3': profile_manager.delete_passenger,
            '4': details_manager.search_passengers,
            '5': details_manager.view_all_passengers
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 