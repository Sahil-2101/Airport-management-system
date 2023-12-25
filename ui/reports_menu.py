from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header

def display_reports_menu() -> None:
    """Display the reports menu options."""
    print_header("Reports")
    print("\nReports features are under construction.")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def handle_reports_menu() -> None:
    """Handle reports menu selection."""
    while True:
        clear_screen()
        display_reports_menu()
        choice = get_valid_input(
            "Enter your choice (6 to go back): ",
            str,
            lambda x: x == '6'
        )
        if choice == '6':
            break 