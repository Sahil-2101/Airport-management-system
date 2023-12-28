from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from src.managers.airport.airport_operations import AirportOperations

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
    airport_manager = AirportOperations()
    
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
            '1': airport_manager.add_airport,
            '2': airport_manager.update_airport,
            '3': airport_manager.delete_airport,
            '4': airport_manager.search_airports,
            '5': airport_manager.view_all_airports
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 