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
                query = "SELECT * FROM employees WHERE name ILIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '2':
                query = "SELECT * FROM employees WHERE department ILIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '3':
                query = "SELECT * FROM employees WHERE position ILIKE %s"
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
        
        for emp in results:
            print(f"{emp[0]:<11} | {emp[1]:<20} | {emp[2]:<15} | {emp[3]:<15} | {emp[4]:<10} | {emp[5]}") 