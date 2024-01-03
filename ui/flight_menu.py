from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from src.managers.flight.schedule import FlightSchedule
from src.managers.flight.search import FlightSearch
from src.managers.flight.status import FlightStatusManager

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
    schedule_manager = FlightSchedule()
    search_manager = FlightSearch()
    status_manager = FlightStatusManager()
    
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
            '1': schedule_manager.add_flight,
            '2': schedule_manager.update_flight,
            '3': schedule_manager.delete_flight,
            '4': search_manager.search_flights,
            '5': schedule_manager.view_flight_schedule
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 