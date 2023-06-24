"""
Seat management module for the Airport Management System.
"""

class SeatManager:
    """Handles seat-related operations."""
    
    def __init__(self, db):
        self.db = db

    def get_available_seats(self, flight_series: str, flight_number: int) -> list:
        """Get list of available seats for a flight."""
        query = """
            SELECT seat_number 
            FROM seats 
            WHERE flight_series = %s 
            AND flight_number = %s 
            AND is_available = TRUE
        """
        result = self.db.execute_query(query, (flight_series, flight_number))
        return [row[0] for row in result] if result else []

    def update_seat_availability(self, flight_series: str, flight_number: int, 
                               seat_number: str, is_available: bool) -> None:
        """Update seat availability status."""
        query = """
            UPDATE seats 
            SET is_available = %s 
            WHERE flight_series = %s 
            AND flight_number = %s 
            AND seat_number = %s
        """
        self.db.execute_query(query, (is_available, flight_series, flight_number, seat_number))

    def update_flight_seats(self, flight_series: str, flight_number: int, increment: bool) -> None:
        """Update the number of available seats for a flight."""
        operation = "available + 1" if increment else "available - 1"
        query = f"""
            UPDATE flight 
            SET available = {operation}
            WHERE flightseries = %s 
            AND flightnumber = %s
        """
        self.db.execute_query(query, (flight_series, flight_number)) 