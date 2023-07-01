"""
Admin management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from .admin import AdminEmployee

class AdminManager:
    """Handles all administrative operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.employee = AdminEmployee(db)

    def display_employee(self, emp_id: int) -> None:
        """Display details of a specific employee."""
        self.employee.display_employee(emp_id)

    def insert_employee(self, emp_id: int, name: str, sales: int, job_id: int) -> None:
        """Insert a new employee record."""
        self.employee.insert_employee(emp_id, name, sales, job_id)

    def update_employee(self, emp_id: int, field: str, new_value: str) -> None:
        """Update specific field of an employee record."""
        self.employee.update_employee(emp_id, field, new_value)

    def delete_employee(self, emp_id: int) -> None:
        """Delete an employee record after confirmation."""
        self.employee.delete_employee(emp_id)

    def list_employees(self, page: int = 1, page_size: int = 5) -> None:
        """List all employees with pagination."""
        self.employee.list_employees(page, page_size)