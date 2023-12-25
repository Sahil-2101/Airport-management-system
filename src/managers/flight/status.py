"""
Flight status management for the Airport Management System.
"""

from enum import Enum
from typing import Optional
from src.database.connection import DatabaseConnection

class FlightStatus(Enum):
    """Enumeration of possible flight statuses."""
    SCHEDULED = "Scheduled"
    BOARDING = "Boarding"
    DEPARTED = "Departed"
    ARRIVED = "Arrived"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"

class FlightStatusManager:
    """Manages flight status updates and queries."""
    
    def __init__(self):
        """Initialize the flight status manager."""
        self.db = DatabaseConnection()
    
    def update_flight_status(self, flight_id: str, status: FlightStatus, delay_minutes: Optional[int] = None) -> bool:
        """
        Update the status of a flight.
        
        Args:
            flight_id: The ID of the flight to update
            status: The new status to set
            delay_minutes: Optional delay in minutes (for DELAYED status)
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if status == FlightStatus.DELAYED and delay_minutes is None:
                raise ValueError("Delay minutes required for DELAYED status")
                
            query = """
                UPDATE flights 
                SET status = %s, delay_minutes = %s
                WHERE flight_id = %s
            """
            params = (status.value, delay_minutes, flight_id)
            
            self.db.execute_query(query, params)
            return True
            
        except Exception as e:
            print(f"Error updating flight status: {e}")
            return False
    
    def get_flight_status(self, flight_id: str) -> Optional[tuple]:
        """
        Get the current status of a flight.
        
        Args:
            flight_id: The ID of the flight to query
            
        Returns:
            tuple: (status, delay_minutes) if found, None otherwise
        """
        try:
            query = "SELECT status, delay_minutes FROM flights WHERE flight_id = %s"
            result = self.db.execute_query(query, (flight_id,))
            
            if result and len(result) > 0:
                return result[0]
            return None
            
        except Exception as e:
            print(f"Error getting flight status: {e}")
            return None 