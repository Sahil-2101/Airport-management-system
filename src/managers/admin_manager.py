"""
Admin management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class AdminManager:
    """Handles all administrative operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def display_employee(self, emp_id: int) -> None:
        """Display details of a specific employee."""
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            for row in result:
                print(row)

    def insert_employee(self, emp_id: int, name: str, sales: int, job_id: int) -> None:
        """Insert a new employee record."""
        query = "INSERT INTO Employee VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (emp_id, name, sales, job_id))

    def update_employee(self, emp_id: int, field: str, new_value: str) -> None:
        """Update specific field of an employee record."""
        query = f"UPDATE Employee SET {field} = %s WHERE employeeid = %s"
        self.db.execute_query(query, (new_value, emp_id))

    def delete_employee(self, emp_id: int) -> None:
        """Delete an employee record after confirmation."""
        # First display the record
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            print(f"Employee details to be deleted: {result[0]}")
            if input("Confirm deletion? (yes/no): ").lower() == 'yes':
                query = "DELETE FROM Employee WHERE employeeid = %s"
                self.db.execute_query(query, (emp_id,))
                print("Record deleted successfully")