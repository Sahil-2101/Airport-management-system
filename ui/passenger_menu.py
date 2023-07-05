from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from passenger_management.passenger_operations import (
    register_passenger, update_passenger,
    delete_passenger, search_passengers,
    view_all_passengers
)

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
            '1': register_passenger,
            '2': update_passenger,
            '3': delete_passenger,
            '4': search_passengers,
            '5': view_all_passengers
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 