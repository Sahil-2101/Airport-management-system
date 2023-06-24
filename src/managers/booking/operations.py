"""
Booking operations module for the Airport Management System.
"""

import uuid
from datetime import datetime

class BookingOperations:
    """Handles core booking operations."""
    
    def __init__(self, db):
        self.db = db

    def _generate_booking_id(self) -> str:
        """Generate a unique booking ID."""
        return str(uuid.uuid4())[:8].upper()

    def create_booking(self, username: str, flight_series: str, flight_number: int,
                      seat_number: str, payment_method: str) -> tuple:
        """Create a new booking record."""
        booking_id = self._generate_booking_id()
        query = """
            INSERT INTO bookings (
                booking_id, username, flight_series, flight_number,
                seat_number, booking_date, payment_method, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            booking_id, username, flight_series, flight_number,
            seat_number, datetime.now(), payment_method, 'CONFIRMED'
        )
        self.db.execute_query(query, params)
        return booking_id

    def get_booking_details(self, booking_id: str) -> tuple:
        """Get detailed booking information."""
        query = """
            SELECT b.*, f.departure, f.arrival, f.departuretime, f.arrivaltime, f.price,
                   pa.email, pa.name
            FROM bookings b
            JOIN flight f ON b.flight_series = f.flightseries 
            AND b.flight_number = f.flightnumber
            JOIN passenger_accounts pa ON b.username = pa.username
            WHERE b.booking_id = %s
        """
        return self.db.execute_query(query, (booking_id,))

    def update_booking_status(self, booking_id: str, new_status: str) -> None:
        """Update the status of a booking."""
        query = "UPDATE bookings SET status = %s WHERE booking_id = %s"
        self.db.execute_query(query, (new_status, booking_id))

    def get_passenger_details(self, username: str) -> tuple:
        """Get passenger account details."""
        query = "SELECT email, name FROM passenger_accounts WHERE username = %s"
        return self.db.execute_query(query, (username,))

    def get_flight_details(self, flight_series: str, flight_number: int) -> tuple:
        """Get flight details."""
        query = """
            SELECT departure, arrival, departuretime, arrivaltime, price 
            FROM flight 
            WHERE flightseries = %s AND flightnumber = %s
        """
        return self.db.execute_query(query, (flight_series, flight_number)) 