"""
Booking manager module for the Airport Management System.
"""

from .booking import BookingNotifier, SeatManager, BookingOperations

class BookingManager:
    """Handles flight booking operations."""
    
    def __init__(self, db):
        self.db = db
        self.notifier = BookingNotifier()
        self.seat_manager = SeatManager(db)
        self.operations = BookingOperations(db)

    def check_available_seats(self, flight_series: str, flight_number: int) -> list:
        """Check available seats for a flight."""
        return self.seat_manager.get_available_seats(flight_series, flight_number)

    def book_flight(self, username: str, flight_series: str, flight_number: int,
                   seat_number: str, payment_method: str) -> str:
        """Book a flight for a passenger."""
        # Check seat availability
        available_seats = self.seat_manager.get_available_seats(flight_series, flight_number)
        if not available_seats or seat_number not in available_seats:
            raise ValueError("Selected seat is not available")

        # Create booking
        booking_id = self.operations.create_booking(
            username, flight_series, flight_number, seat_number, payment_method
        )

        # Update seat availability
        self.seat_manager.update_seat_availability(flight_series, flight_number, seat_number, False)
        self.seat_manager.update_flight_seats(flight_series, flight_number, -1)

        # Get booking details for email
        booking_details = self.operations.get_booking_details(booking_id)
        passenger_details = self.operations.get_passenger_details(username)
        flight_details = self.operations.get_flight_details(flight_series, flight_number)

        # Send confirmation email
        self.notifier.send_booking_confirmation(
            booking_id, booking_details, passenger_details, flight_details
        )

        return booking_id

    def cancel_booking(self, booking_id: str) -> None:
        """Cancel a flight booking."""
        # Get booking details
        booking_details = self.operations.get_booking_details(booking_id)
        if not booking_details:
            raise ValueError("Booking not found")

        # Update booking status
        self.operations.update_booking_status(booking_id, 'CANCELLED')

        # Update seat availability
        self.seat_manager.update_seat_availability(
            booking_details[2], booking_details[3], booking_details[4], True
        )
        self.seat_manager.update_flight_seats(booking_details[2], booking_details[3], 1)

    def view_booking_details(self, booking_id: str) -> None:
        """View details of a booking."""
        booking_details = self.operations.get_booking_details(booking_id)
        if not booking_details:
            print("Booking not found")
            return

        print("\nBooking Details:")
        print(f"Booking ID: {booking_details[0]}")
        print(f"Passenger: {booking_details[8]}")  # Name from passenger_accounts
        print(f"Flight: {booking_details[2]}{booking_details[3]}")
        print(f"Route: {booking_details[4]} to {booking_details[5]}")
        print(f"Departure: {booking_details[6]}")
        print(f"Arrival: {booking_details[7]}")
        print(f"Seat: {booking_details[4]}")
        print(f"Status: {booking_details[7]}")
        print(f"Payment Method: {booking_details[5]}")
        print(f"Booking Date: {booking_details[6]}") 