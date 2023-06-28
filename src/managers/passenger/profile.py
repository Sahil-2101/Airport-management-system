"""
Profile management for passenger accounts.
"""

from datetime import datetime

class PassengerProfile:
    def __init__(self, db):
        self.db = db

    def create_account(self, username: str, hashed_password: str, email: str, name: str, phone: str) -> bool:
        """Create a new passenger account. Assumes password is already hashed."""
        # Check if username already exists
        query = "SELECT * FROM passenger_accounts WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        if result:
            print("Username already exists")
            return False
        # Insert new account
        query = """INSERT INTO passenger_accounts \
                  (username, password, email, name, phone, created_at) \
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

    def view_profile(self, username: str) -> None:
        """Display passenger profile information."""
        query = """SELECT username, email, name, phone, created_at \
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