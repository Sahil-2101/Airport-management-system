"""
Employee profile management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class EmployeeProfile:
    """Handles employee profile operations."""
    
    def __init__(self):
        """Initialize the employee profile manager."""
        self.db = DatabaseConnection()
    
    def add_employee(self) -> None:
        """Add a new employee to the system."""
        print("\nAdd New Employee")
        print("-" * 50)
        
        # Get employee details
        name = input("Enter employee name: ")
        position = input("Enter position: ")
        department = input("Enter department: ")
        contact = input("Enter contact number: ")
        email = input("Enter email: ")
        
        try:
            query = """
                INSERT INTO employees (name, position, department, contact, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (name, position, department, contact, email)
            self.db.execute_query(query, params)
            print("\nEmployee added successfully!")
            
        except Exception as e:
            print(f"\nError adding employee: {str(e)}")
    
    def update_employee(self) -> None:
        """Update an existing employee's details."""
        print("\nUpdate Employee")
        print("-" * 50)
        
        # Get employee ID
        emp_id = input("Enter employee ID to update: ")
        
        # Get updated details
        name = input("Enter new name (press Enter to skip): ")
        position = input("Enter new position (press Enter to skip): ")
        department = input("Enter new department (press Enter to skip): ")
        contact = input("Enter new contact number (press Enter to skip): ")
        email = input("Enter new email (press Enter to skip): ")
        
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = %s")
                params.append(name)
            if position:
                updates.append("position = %s")
                params.append(position)
            if department:
                updates.append("department = %s")
                params.append(department)
            if contact:
                updates.append("contact = %s")
                params.append(contact)
            if email:
                updates.append("email = %s")
                params.append(email)
            
            if updates:
                query = f"""
                    UPDATE employees 
                    SET {', '.join(updates)}
                    WHERE employee_id = %s
                """
                params.append(emp_id)
                self.db.execute_query(query, tuple(params))
                print("\nEmployee updated successfully!")
            else:
                print("\nNo updates provided.")
                
        except Exception as e:
            print(f"\nError updating employee: {str(e)}")
    
    def delete_employee(self) -> None:
        """Delete an employee from the system."""
        print("\nDelete Employee")
        print("-" * 50)
        
        emp_id = input("Enter employee ID to delete: ")
        confirm = input("Are you sure you want to delete this employee? (y/n): ")
        
        if confirm.lower() == 'y':
            try:
                query = "DELETE FROM employees WHERE employee_id = %s"
                self.db.execute_query(query, (emp_id,))
                print("\nEmployee deleted successfully!")
                
            except Exception as e:
                print(f"\nError deleting employee: {str(e)}")
        else:
            print("\nDeletion cancelled.") 