from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from airport_management.airport_operations import (
    add_airport, update_airport,
    delete_airport, search_airports,
    view_all_airports
)

def display_airport_menu() -> None:
    """Display the airport management menu options."""
    print_header("Airport Management")
    print("\n1. Add New Airport")
    print("2. Update Airport")
    print("3. Delete Airport")
    print("4. Search Airports")
    print("5. View All Airports")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def handle_airport_menu() -> None:
    """Handle airport management menu selection."""
    while True:
        clear_screen()
        display_airport_menu()
        choice = get_valid_input(
            "Enter your choice (1-6): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5', '6']
        )
        
        if choice == '6':
            break
            
        menu_handlers: Dict[str, Callable] = {
            '1': add_airport,
            '2': update_airport,
            '3': delete_airport,
            '4': search_airports,
            '5': view_all_airports
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 