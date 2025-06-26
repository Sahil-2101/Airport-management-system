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
            # A simpler approach: fetch all statuses and count in Python
            query = "SELECT status FROM flights"
            results = self.db.execute_query(query)
            
            if results:
                # Initialize a dictionary to hold status counts
                status_counts = {
                    'total_flights': 0,
                    'scheduled': 0,
                    'on_time': 0,
                    'departed': 0,
                    'arrived': 0,
                    'delayed': 0,
                    'cancelled': 0
                }

                # Count statuses in Python
                for row in results:
                    status = row[0]
                    status_counts['total_flights'] += 1
                    if status == 'Scheduled':
                        status_counts['scheduled'] += 1
                    elif status == 'ON TIME':
                        status_counts['on_time'] += 1
                    elif status == 'Departed':
                        status_counts['departed'] += 1
                    elif status == 'Arrived':
                        status_counts['arrived'] += 1
                    elif status == 'Delayed':
                        status_counts['delayed'] += 1
                    elif status == 'Cancelled':
                        status_counts['cancelled'] += 1

                print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("\nFlight Statistics:")
                print(f"Total Flights: {status_counts['total_flights']}")
                print(f"Scheduled: {status_counts['scheduled']}")
                print(f"On Time: {status_counts['on_time']}")
                print(f"Departed: {status_counts['departed']}")
                print(f"Arrived: {status_counts['arrived']}")
                print(f"Delayed: {status_counts['delayed']}")
                print(f"Cancelled: {status_counts['cancelled']}")
            else:
                print("Could not retrieve flight statistics.")
            
        except Exception as e:
            print(f"\nError generating flight report: {str(e)}")
    
    def generate_passenger_report(self) -> None:
        """Generate a report of passenger statistics."""
        print("\nPassenger Statistics Report")
        print("-" * 50)
        
        try:
            # Get passenger statistics from the bookings table
            query = """
                SELECT 
                    COUNT(DISTINCT username) as total_passengers,
                    COUNT(DISTINCT CONCAT(flight_series, flight_number)) as total_flights_with_bookings,
                    COUNT(*) as total_bookings
                FROM bookings
            """
            stats_result = self.db.execute_query(query)

            if stats_result:
                stats = stats_result[0]
                print(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("\nPassenger Statistics:")
                print(f"Total Unique Passengers with Bookings: {stats[0]}")
                print(f"Total Flights with Bookings: {stats[1]}")
                print(f"Total Bookings: {stats[2]}")
            else:
                print("Could not retrieve passenger statistics.")
            
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