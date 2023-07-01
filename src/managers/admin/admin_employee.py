"""
Admin employee operations module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class AdminEmployee:
    """Handles all employee-related admin operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def display_employee(self, emp_id: int) -> None:
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            for row in result:
                print(row)

    def insert_employee(self, emp_id: int, name: str, sales: int, job_id: int) -> None:
        query = "INSERT INTO Employee VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (emp_id, name, sales, job_id))

    def update_employee(self, emp_id: int, field: str, new_value: str) -> None:
        query = f"UPDATE Employee SET {field} = %s WHERE employeeid = %s"
        self.db.execute_query(query, (new_value, emp_id))

    def delete_employee(self, emp_id: int) -> None:
        query = "SELECT * FROM Employee WHERE employeeid = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result:
            print(f"Employee details to be deleted: {result[0]}")
            if input("Confirm deletion? (yes/no): ").lower() == 'yes':
                query = "DELETE FROM Employee WHERE employeeid = %s"
                self.db.execute_query(query, (emp_id,))
                print("Record deleted successfully")

    def list_employees(self, page: int = 1, page_size: int = 5) -> None:
        offset = (page - 1) * page_size
        query = "SELECT * FROM Employee ORDER BY employeeid LIMIT %s OFFSET %s"
        result = self.db.execute_query(query, (page_size, offset))
        if result:
            print(f"\nEmployee List (Page {page}):")
            print("ID\tName\tSales\tJob ID")
            for row in result:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
        else:
            print("No employees found on this page.") 