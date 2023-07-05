from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header

def display_main_menu() -> None:
    """Display the main menu options."""
    print_header("Airport Management System")
    print("\n1. Flight Management")
    print("2. Passenger Management")
    print("3. Employee Management")
    print("4. Airport Management")
    print("5. Reports")
    print("6. Exit")
    print("\n" + "="*50)

def handle_main_menu() -> str:
    """Handle main menu selection and return the choice."""
    while True:
        display_main_menu()
        choice = get_valid_input(
            "Enter your choice (1-6): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5', '6']
        )
        return choice

def get_menu_handler(choice: str) -> Callable:
    """Get the appropriate menu handler based on user choice."""
    menu_handlers: Dict[str, Callable] = {
        '1': handle_flight_menu,
        '2': handle_passenger_menu,
        '3': handle_employee_menu,
        '4': handle_airport_menu,
        '5': handle_reports_menu
    }
    return menu_handlers.get(choice)

def handle_flight_menu() -> None:
    """Handle flight management menu."""
    from ui.flight_menu import handle_flight_menu
    handle_flight_menu()

def handle_passenger_menu() -> None:
    """Handle passenger management menu."""
    from ui.passenger_menu import handle_passenger_menu
    handle_passenger_menu()

def handle_employee_menu() -> None:
    """Handle employee management menu."""
    from ui.employee_menu import handle_employee_menu
    handle_employee_menu()

def handle_airport_menu() -> None:
    """Handle airport management menu."""
    from ui.airport_menu import handle_airport_menu
    handle_airport_menu()

def handle_reports_menu() -> None:
    """Handle reports menu."""
    from ui.reports_menu import handle_reports_menu
    handle_reports_menu() 