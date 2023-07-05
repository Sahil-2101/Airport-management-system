from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from flight_management.flight_operations import (
    add_flight, update_flight, delete_flight,
    search_flights, view_all_flights
)

def display_flight_menu() -> None:
    """Display the flight management menu options."""
    print_header("Flight Management")
    print("\n1. Add New Flight")
    print("2. Update Flight")
    print("3. Delete Flight")
    print("4. Search Flights")
    print("5. View All Flights")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def handle_flight_menu() -> None:
    """Handle flight management menu selection."""
    while True:
        clear_screen()
        display_flight_menu()
        choice = get_valid_input(
            "Enter your choice (1-6): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5', '6']
        )
        
        if choice == '6':
            break
            
        menu_handlers: Dict[str, Callable] = {
            '1': add_flight,
            '2': update_flight,
            '3': delete_flight,
            '4': search_flights,
            '5': view_all_flights
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 