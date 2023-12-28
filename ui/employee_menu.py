from typing import Callable, Dict
from utils.validators import get_valid_input
from utils.helpers import clear_screen, print_header
from src.managers.employee.profile import EmployeeProfile
from src.managers.employee.employee_details import EmployeeDetails

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
    profile_manager = EmployeeProfile()
    details_manager = EmployeeDetails()
    
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
            '1': profile_manager.add_employee,
            '2': profile_manager.update_employee,
            '3': profile_manager.delete_employee,
            '4': details_manager.search_employees,
            '5': details_manager.view_all_employees
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
            input("\nPress Enter to continue...") 