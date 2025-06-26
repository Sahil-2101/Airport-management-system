"""
Database connection handler for the Airport Management System.
"""

import mysql.connector
from typing import List, Optional
from .config import DB_CONFIG
import os

class DatabaseConnection:
    """Handles database connection and cursor operations."""
    
    def __init__(self):
        """Initialize database connection and cursor. Automatically create database and tables if missing."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to database")
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            # If the error is unknown database, try to create it
            if e.errno == 1049:  # Unknown database
                print("Database does not exist. Attempting to create database and tables...")
                self._initialize_schema()
                # Try connecting again
                self.connection = mysql.connector.connect(**DB_CONFIG)
                if self.connection.is_connected():
                    print("Successfully connected to database after initialization.")
                self.cursor = self.connection.cursor()
            else:
                print(f"Error connecting to database: {e}")
                raise

    def _initialize_schema(self):
        """Run the schema.sql file to create the database and tables."""
        # Connect without specifying database
        config_no_db = DB_CONFIG.copy()
        db_name = config_no_db.pop("database")
        connection = mysql.connector.connect(**config_no_db)
        cursor = connection.cursor()

        try:
            print(f"Dropping database '{db_name}' if it exists...")
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            print(f"Database '{db_name}' dropped.")
        except mysql.connector.Error as e:
            print(f"Error dropping database: {e}")
            # This might fail if the user doesn't have permissions, but we can proceed
            pass

        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            print("Executing schema script...")
            # Split the script into individual statements as the 'multi' parameter is not supported by your library version
            sql_commands = f.read().split(';')
            for command in sql_commands:
                cmd = command.strip()
                if cmd:
                    try:
                        cursor.execute(cmd)
                    except mysql.connector.Error as e:
                        # Ignore 'no result set to fetch' which can happen with USE statements
                        if e.errno != 2014:
                             print(f"Error executing schema command: {e}\nCommand: {cmd}")
            print("Schema script executed successfully.")

        connection.commit()
        cursor.close()
        connection.close()

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