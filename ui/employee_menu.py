from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from employee_management.employee_operations import (
    add_employee, update_employee,
    delete_employee, search_employees,
    view_all_employees
)

def display_employee_menu() -> None:
    """Display the employee management menu options."""
    print_header("Employee Management")
    print("\n1. Add New Employee")
    print("2. Update Employee")
    print("3. Delete Employee")
    print("4. Search Employees")
    print("5. View All Employees")
    print("6. Back to Main Menu")
    print("\n" + "="*50)

def handle_employee_menu() -> None:
    """Handle employee management menu selection."""
    while True:
        clear_screen()
        display_employee_menu()
        choice = get_valid_input(
            "Enter your choice (1-6): ",
            str,
            lambda x: x in ['1', '2', '3', '4', '5', '6']
        )
        
        if choice == '6':
            break
            
        menu_handlers: Dict[str, Callable] = {
            '1': add_employee,
            '2': update_employee,
            '3': delete_employee,
            '4': search_employees,
            '5': view_all_employees
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 