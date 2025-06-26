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

    def delete_account(self, username: str) -> bool:
        """Delete a passenger account."""
        query = "DELETE FROM passenger_accounts WHERE username = %s"
        try:
            # It's good practice to check how many rows were affected.
            self.db.execute_query(query, (username,))
            # The mysql-connector-python cursor.rowcount property can be used
            # if the execute_query method is adapted to return it for DELETE.
            # For now, we assume success if no exception is raised.
            print(f"Account '{username}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting account: {e}")
            return False

    def view_all_profiles(self) -> None:
        """View all passenger profiles in the system."""
        print("\nAll Passenger Profiles")
        print("-" * 50)
        
        try:
            query = "SELECT username, name, email, phone, created_at FROM passenger_accounts ORDER BY username"
            results = self.db.execute_query(query)
            self._display_profile_results(results)
            
        except Exception as e:
            print(f"\nError viewing profiles: {str(e)}")
    
    def _display_profile_results(self, results) -> None:
        """Display passenger profile results in a formatted table."""
        if not results:
            print("\nNo passenger profiles found.")
            return
            
        print("\nUsername   | Name                 | Email                | Phone        | Member Since")
        print("-" * 80)
        
        def format_cell(data, width, align='<'):
            """Safely format cell data, handling None values."""
            if data is None:
                return f"{'N/A':{align}{width}}"
            return f"{str(data):{align}{width}}"

        for row in results:
            username = format_cell(row[0], 10)
            name = format_cell(row[1], 20)
            email = format_cell(row[2], 20)
            phone = format_cell(row[3], 12)
            created_at = format_cell(row[4], 0) 
            print(f"{username} | {name} | {email} | {phone} | {created_at}") 