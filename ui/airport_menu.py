from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header

def display_airport_menu() -> None:
    """Display the airport management menu options."""
    print_header("Airport Management")
    print("\nAirport management features are under construction.")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def handle_airport_menu() -> None:
    """Handle airport management menu selection."""
    while True:
        clear_screen()
        display_airport_menu()
        choice = get_valid_input(
            "Enter your choice (6 to go back): ",
            str,
            lambda x: x == '6'
        )
        if choice == '6':
            break 