from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from reports.report_operations import (
    generate_flight_report,
    generate_passenger_report,
    generate_employee_report,
    generate_airport_report
)

def display_reports_menu() -> None:
    """Display the reports menu options."""
    print_header("Reports")
    print("\n1. Flight Reports")
    print("2. Passenger Reports")
    print("3. Employee Reports")
    print("4. Airport Reports")
    print("5. Back to Main Menu")
    print("\n" + "="*50)

def handle_reports_menu() -> None:
    """Handle reports menu selection."""
    while True:
        clear_screen()
        display_reports_menu()
        choice = get_valid_input(
            "Enter your choice (1-5): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5']
        )
        
        if choice == '5':
            break
            
        menu_handlers: Dict[str, Callable] = {
            '1': generate_flight_report,
            '2': generate_passenger_report,
            '3': generate_employee_report,
            '4': generate_airport_report
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 