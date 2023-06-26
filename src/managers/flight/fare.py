"""
Flight fare calculation module for the Airport Management System.
"""

class FareCalculator:
    """Handles flight fare calculations based on distance, duration, and stops."""
    
    @staticmethod
    def calculate_fare(distance: float, duration: int, stops: int) -> float:
        """
        Calculate flight fare based on distance, duration, and number of stops.
        
        Args:
            distance (float): Flight distance in kilometers
            duration (int): Flight duration in minutes
            stops (int): Number of stops (0-2)
            
        Returns:
            float: Calculated fare
        """
        if stops not in [0, 1, 2]:
            raise ValueError("Stops must be 0, 1, or 2.")
            
        base_fare = distance * 0.1 + duration * 0.05
        return base_fare * (1 - 0.15 * stops) 