"""
Employee details management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class EmployeeDetails:
    """Handles employee search and view operations."""
    
    def __init__(self):
        """Initialize the employee details manager."""
        self.db = DatabaseConnection()
    
    def search_employees(self) -> None:
        """Search for employees based on various criteria."""
        print("\nSearch Employees")
        print("-" * 50)
        
        print("\nSearch by:")
        print("1. Name")
        print("2. Department")
        print("3. Position")
        print("4. Back")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '4':
            return
            
        search_term = input("Enter search term: ")
        
        try:
            if choice == '1':
                query = "SELECT * FROM employees WHERE name LIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '2':
                query = "SELECT * FROM employees WHERE department LIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '3':
                query = "SELECT * FROM employees WHERE position LIKE %s"
                params = (f'%{search_term}%',)
            else:
                print("\nInvalid choice!")
                return
            
            results = self.db.execute_query(query, params)
            self._display_employee_results(results)
            
        except Exception as e:
            print(f"\nError searching employees: {str(e)}")
    
    def view_all_employees(self) -> None:
        """View all employees in the system."""
        print("\nAll Employees")
        print("-" * 50)
        
        try:
            query = "SELECT * FROM employees ORDER BY employee_id"
            results = self.db.execute_query(query)
            self._display_employee_results(results)
            
        except Exception as e:
            print(f"\nError viewing employees: {str(e)}")
    
    def _display_employee_results(self, results) -> None:
        """Display employee search results in a formatted table."""
        if not results:
            print("\nNo employees found.")
            return
            
        print("\nEmployee ID | Name | Position | Department | Contact | Email")
        print("-" * 80)
        
        def format_cell(data, width, align='<'):
            """Safely format cell data, handling None values."""
            if data is None:
                return f"{'N/A':{align}{width}}"
            return f"{str(data):{align}{width}}"

        for emp in results:
            emp_id = format_cell(emp[0], 11)
            name = format_cell(emp[1], 20)
            position = format_cell(emp[2], 15)
            department = format_cell(emp[3], 15)
            contact = format_cell(emp[4], 10)
            email = format_cell(emp[5], 0)  # No padding for the last item
            print(f"{emp_id} | {name} | {position} | {department} | {contact} | {email}") 