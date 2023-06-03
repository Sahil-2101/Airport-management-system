"""
Database connection handler for the Airport Management System.
"""

import mysql.connector
from typing import List, Optional
from .config import DB_CONFIG

class DatabaseConnection:
    """Handles database connection and cursor operations."""
    
    def __init__(self):
        """Initialize database connection and cursor."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to database")
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: tuple = None) -> Optional[List]:
        """Execute a database query and return results."""
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                return self.cursor.fetchall()
            self.connection.commit()
            return None
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return None 