"""
Passenger account management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from datetime import datetime
import hashlib

class PassengerAccountManager:
    """Handles all passenger account operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, username: str, password: str, email: str, 
                      name: str, phone: str) -> bool:
        """Create a new passenger account."""
        # Check if username already exists
        query = "SELECT * FROM passenger_accounts WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        if result:
            print("Username already exists")
            return False

        # Hash the password
        hashed_password = self._hash_password(password)
        
        # Insert new account
        query = """INSERT INTO passenger_accounts 
                  (username, password, email, name, phone, created_at) 
                  VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (username, hashed_password, email, name, phone, 
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        try:
            self.db.execute_query(query, params)
            print("Account created successfully!")
            return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False

    def login(self, username: str, password: str) -> bool:
        """Authenticate a passenger account."""
        hashed_password = self._hash_password(password)
        query = "SELECT * FROM passenger_accounts WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, hashed_password))
        
        if result:
            print(f"Welcome back, {result[0][3]}!")  # result[0][3] is the name
            return True
        else:
            print("Invalid username or password")
            return False

    def update_profile(self, username: str, field: str, new_value: str) -> bool:
        """Update passenger profile information."""
        allowed_fields = ['email', 'phone', 'name']
        if field not in allowed_fields:
            print(f"Invalid field. Allowed fields: {', '.join(allowed_fields)}")
            return False

        query = f"UPDATE passenger_accounts SET {field} = %s WHERE username = %s"
        try:
            self.db.execute_query(query, (new_value, username))
            print(f"{field.capitalize()} updated successfully!")
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        """Change passenger account password."""
        # Verify current password
        current_hash = self._hash_password(current_password)
        query = "SELECT * FROM passenger_accounts WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, current_hash))
        
        if not result:
            print("Current password is incorrect")
            return False

        # Update to new password
        new_hash = self._hash_password(new_password)
        query = "UPDATE passenger_accounts SET password = %s WHERE username = %s"
        try:
            self.db.execute_query(query, (new_hash, username))
            print("Password changed successfully!")
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False

    def view_profile(self, username: str) -> None:
        """Display passenger profile information."""
        query = """SELECT username, email, name, phone, created_at 
                  FROM passenger_accounts WHERE username = %s"""
        result = self.db.execute_query(query, (username,))
        
        if result:
            print("\nProfile Information:")
            print(f"Username: {result[0][0]}")
            print(f"Name: {result[0][2]}")
            print(f"Email: {result[0][1]}")
            print(f"Phone: {result[0][3]}")
            print(f"Member since: {result[0][4]}")
        else:
            print("Profile not found")

    def view_booking_history(self, username: str) -> None:
        """Display passenger's booking history."""
        query = """
            SELECT f.flightseries, f.flightnumber, f.departure, f.arrival,
                   f.departuretime, f.arrivaltime, f.status
            FROM passenger_accounts pa
            JOIN passenger p ON pa.name = p.name
            JOIN flight f ON p.flightserial = f.flightseries 
            AND p.flightnumber = f.flightnumber
            WHERE pa.username = %s
            ORDER BY f.departuretime DESC
        """
        result = self.db.execute_query(query, (username,))
        
        if result:
            print("\nBooking History:")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")
        else:
            print("No booking history found") 