"""
Report operations management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from datetime import datetime

class ReportOperations:
    """Handles report generation operations."""
    
    def __init__(self):
        """Initialize the report operations manager."""
        self.db = DatabaseConnection()
    
    def generate_flight_report(self) -> None:
        """Generate a report of flight operations."""
        print("\nFlight Operations Report")
        print("-" * 50)
        
        try:
            # Get flight statistics
            query = """
                SELECT 
                    COUNT(*) as total_flights,
                    COUNT(CASE WHEN status = 'Scheduled' THEN 1 END) as scheduled,
                    COUNT(CASE WHEN status = 'Boarding' THEN 1 END) as boarding,
                    COUNT(CASE WHEN status = 'Departed' THEN 1 END) as departed,
                    COUNT(CASE WHEN status = 'Arrived' THEN 1 END) as arrived,
                    COUNT(CASE WHEN status = 'Delayed' THEN 1 END) as delayed,
                    COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) as cancelled
                FROM flights
            """
            stats = self.db.execute_query(query)[0]
            
            print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nFlight Statistics:")
            print(f"Total Flights: {stats[0]}")
            print(f"Scheduled: {stats[1]}")
            print(f"Boarding: {stats[2]}")
            print(f"Departed: {stats[3]}")
            print(f"Arrived: {stats[4]}")
            print(f"Delayed: {stats[5]}")
            print(f"Cancelled: {stats[6]}")
            
        except Exception as e:
            print(f"\nError generating flight report: {str(e)}")
    
    def generate_passenger_report(self) -> None:
        """Generate a report of passenger statistics."""
        print("\nPassenger Statistics Report")
        print("-" * 50)
        
        try:
            # Get passenger statistics
            query = """
                SELECT 
                    COUNT(*) as total_passengers,
                    COUNT(DISTINCT flight_id) as total_flights,
                    COUNT(*) / COUNT(DISTINCT flight_id) as avg_passengers_per_flight
                FROM passengers
            """
            stats = self.db.execute_query(query)[0]
            
            print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nPassenger Statistics:")
            print(f"Total Passengers: {stats[0]}")
            print(f"Total Flights: {stats[1]}")
            print(f"Average Passengers per Flight: {stats[2]:.2f}")
            
        except Exception as e:
            print(f"\nError generating passenger report: {str(e)}")
    
    def generate_employee_report(self) -> None:
        """Generate a report of employee statistics."""
        print("\nEmployee Statistics Report")
        print("-" * 50)
        
        try:
            # Get employee statistics by department
            query = """
                SELECT 
                    department,
                    COUNT(*) as employee_count
                FROM employees
                GROUP BY department
                ORDER BY employee_count DESC
            """
            results = self.db.execute_query(query)
            
            print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nEmployee Statistics by Department:")
            print("Department | Employee Count")
            print("-" * 30)
            
            for dept in results:
                print(f"{dept[0]:<10} | {dept[1]}")
            
        except Exception as e:
            print(f"\nError generating employee report: {str(e)}")
    
    def generate_airport_report(self) -> None:
        """Generate a report of airport statistics."""
        print("\nAirport Statistics Report")
        print("-" * 50)
        
        try:
            # Get airport statistics
            query = """
                SELECT 
                    COUNT(*) as total_airports,
                    COUNT(DISTINCT country) as total_countries,
                    SUM(terminals) as total_terminals
                FROM airports
            """
            stats = self.db.execute_query(query)[0]
            
            print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nAirport Statistics:")
            print(f"Total Airports: {stats[0]}")
            print(f"Total Countries: {stats[1]}")
            print(f"Total Terminals: {stats[2]}")
            
        except Exception as e:
            print(f"\nError generating airport report: {str(e)}") 