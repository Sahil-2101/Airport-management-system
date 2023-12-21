"""
Booking logic for passenger accounts.
"""
from ..booking.notifications import BookingNotifier

class PassengerBooking:
    def __init__(self, db, notifier: BookingNotifier):
        self.db = db
        self.notifier = notifier

    def book_flight(self, username: str, flight_series: str, flight_number: int, seat_number: str, payment_method: str) -> None:
        """Book a flight and send confirmation email."""
        # Get passenger email and flight details
        query = "SELECT email FROM passenger_accounts WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        if result:
            recipient_email = result[0][0]
            flight_query = """
                SELECT departure, arrival, departuretime, arrivaltime, price 
                FROM flight 
                WHERE flightseries = %s AND flightnumber = %s
            """
            flight_result = self.db.execute_query(flight_query, (flight_series, flight_number))
            if flight_result:
                flight_details = {
                    'flight_series': flight_series,
                    'flight_number': flight_number,
                    'departure': flight_result[0][0],
                    'arrival': flight_result[0][1],
                    'departure_time': flight_result[0][2],
                    'arrival_time': flight_result[0][3],
                    'price': flight_result[0][4],
                    'seat_number': seat_number
                }
                self.notifier.send_booking_confirmation(recipient_email, "TEMP_ID", flight_details)
        else:
            print("User email not found.") 