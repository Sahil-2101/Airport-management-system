# Airport Management System

A comprehensive airport management system built with Python that handles flight operations, passenger management, employee management, airport operations, and reporting.

## Features

### 1. Flight Management
- Add new flights with details like flight series, number, departure/arrival airports, times, and pricing
- Update existing flight information
- Delete flights from the system
- Search flights based on various criteria
- View complete flight schedules
- Manage flight statuses (Scheduled, Boarding, Departed, Arrived, Delayed, Cancelled)
- Calculate flight fares based on distance, duration, and stops

### 2. Passenger Management
- Register new passengers
- Update passenger information
- Delete passenger records
- Search passengers
- View all passenger records
- Manage passenger bookings
- Handle passenger cancellations
- Send booking confirmations and notifications

### 3. Employee Management
- Add new employees with details like name, position, department, and contact information
- Update employee records
- Delete employee records
- Search employees by various criteria
- View all employee records
- Manage employee profiles and details

### 4. Airport Management
- Add new airports with details like code, name, city, country, and terminals
- Update airport information
- Delete airport records
- Search airports by code, city, or country
- View all airport records

### 5. Reporting System
- Generate flight operation reports
  - Total flights
  - Flights by status
  - Scheduled, boarding, departed, arrived, delayed, and cancelled flights
- Generate passenger statistics
  - Total passengers
  - Average passengers per flight
- Generate employee statistics
  - Employee count by department
- Generate airport statistics
  - Total airports
  - Airports by country
  - Total terminals

## Technical Features

### Database Integration
- PostgreSQL database integration
- Secure database connections
- Efficient query execution
- Transaction management

### User Interface
- Clean and intuitive command-line interface
- Menu-driven navigation
- Input validation
- Clear error messages
- Formatted output display

### Code Structure
- Modular design
- Separation of concerns
- Organized package structure:
  ```
  src/
  ├── managers/
  │   ├── flight/
  │   ├── passenger/
  │   ├── employee/
  │   ├── airport/
  │   └── reports/
  ├── database/
  └── utils/
  ```

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Database error management
- Input validation

## Requirements

- Python 3.8+
- PostgreSQL database
- Required Python packages:
  - psycopg2 (PostgreSQL adapter)
  - datetime
  - typing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/airport-management-system.git
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Create a new database
   - Run the database initialization script

4. Configure database connection:
   - Update database credentials in the configuration file

## Usage

1. Run the main application:
   ```bash
   python main.py
   ```

2. Navigate through the menu system:
   - Use number keys to select options
   - Follow on-screen prompts
   - Press Enter to continue

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
