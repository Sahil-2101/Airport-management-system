"""
Authentication and password management for passenger accounts.
"""

import hashlib

class PassengerAuth:
    def __init__(self, db):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

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