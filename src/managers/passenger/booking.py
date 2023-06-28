"""
Booking logic for passenger accounts.
"""
from .notifications import PassengerNotifier

class PassengerBooking:
    def __init__(self, db, notifier: PassengerNotifier):
        self.db = db
        self.notifier = notifier

    def book_flight(self, username: str, flight_series: str, flight_number: int, seat_number: str, payment_method: str) -> None:
        """Book a flight and send confirmation email."""
        # Get passenger email
        query = "SELECT email FROM passenger_accounts WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        if result:
            recipient_email = result[0][0]
            booking_details = f"Flight: {flight_series}{flight_number}, Seat: {seat_number}, Payment Method: {payment_method}"
            self.notifier.send_confirmation_email(recipient_email, booking_details)
        else:
            print("User email not found.") 