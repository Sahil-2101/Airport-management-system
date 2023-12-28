"""
Airport operations management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class AirportOperations:
    """Handles airport management operations."""
    
    def __init__(self):
        """Initialize the airport operations manager."""
        self.db = DatabaseConnection()
    
    def add_airport(self) -> None:
        """Add a new airport to the system."""
        print("\nAdd New Airport")
        print("-" * 50)
        
        # Get airport details
        code = input("Enter airport code (e.g., JFK): ").upper()
        name = input("Enter airport name: ")
        city = input("Enter city: ")
        country = input("Enter country: ")
        terminals = input("Enter number of terminals: ")
        
        try:
            query = """
                INSERT INTO airports (code, name, city, country, terminals)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (code, name, city, country, terminals)
            self.db.execute_query(query, params)
            print("\nAirport added successfully!")
            
        except Exception as e:
            print(f"\nError adding airport: {str(e)}")
    
    def update_airport(self) -> None:
        """Update an existing airport's details."""
        print("\nUpdate Airport")
        print("-" * 50)
        
        code = input("Enter airport code to update: ").upper()
        
        # Get updated details
        name = input("Enter new name (press Enter to skip): ")
        city = input("Enter new city (press Enter to skip): ")
        country = input("Enter new country (press Enter to skip): ")
        terminals = input("Enter new number of terminals (press Enter to skip): ")
        
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = %s")
                params.append(name)
            if city:
                updates.append("city = %s")
                params.append(city)
            if country:
                updates.append("country = %s")
                params.append(country)
            if terminals:
                updates.append("terminals = %s")
                params.append(terminals)
            
            if updates:
                query = f"""
                    UPDATE airports 
                    SET {', '.join(updates)}
                    WHERE code = %s
                """
                params.append(code)
                self.db.execute_query(query, tuple(params))
                print("\nAirport updated successfully!")
            else:
                print("\nNo updates provided.")
                
        except Exception as e:
            print(f"\nError updating airport: {str(e)}")
    
    def delete_airport(self) -> None:
        """Delete an airport from the system."""
        print("\nDelete Airport")
        print("-" * 50)
        
        code = input("Enter airport code to delete: ").upper()
        confirm = input("Are you sure you want to delete this airport? (y/n): ")
        
        if confirm.lower() == 'y':
            try:
                query = "DELETE FROM airports WHERE code = %s"
                self.db.execute_query(query, (code,))
                print("\nAirport deleted successfully!")
                
            except Exception as e:
                print(f"\nError deleting airport: {str(e)}")
        else:
            print("\nDeletion cancelled.")
    
    def search_airports(self) -> None:
        """Search for airports based on various criteria."""
        print("\nSearch Airports")
        print("-" * 50)
        
        print("\nSearch by:")
        print("1. Code")
        print("2. City")
        print("3. Country")
        print("4. Back")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '4':
            return
            
        search_term = input("Enter search term: ")
        
        try:
            if choice == '1':
                query = "SELECT * FROM airports WHERE code ILIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '2':
                query = "SELECT * FROM airports WHERE city ILIKE %s"
                params = (f'%{search_term}%',)
            elif choice == '3':
                query = "SELECT * FROM airports WHERE country ILIKE %s"
                params = (f'%{search_term}%',)
            else:
                print("\nInvalid choice!")
                return
            
            results = self.db.execute_query(query, params)
            self._display_airport_results(results)
            
        except Exception as e:
            print(f"\nError searching airports: {str(e)}")
    
    def view_all_airports(self) -> None:
        """View all airports in the system."""
        print("\nAll Airports")
        print("-" * 50)
        
        try:
            query = "SELECT * FROM airports ORDER BY code"
            results = self.db.execute_query(query)
            self._display_airport_results(results)
            
        except Exception as e:
            print(f"\nError viewing airports: {str(e)}")
    
    def _display_airport_results(self, results) -> None:
        """Display airport search results in a formatted table."""
        if not results:
            print("\nNo airports found.")
            return
            
        print("\nCode | Name | City | Country | Terminals")
        print("-" * 60)
        
        for airport in results:
            print(f"{airport[0]:<5} | {airport[1]:<20} | {airport[2]:<15} | {airport[3]:<15} | {airport[4]}") 