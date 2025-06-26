-- Create database if not exists
CREATE DATABASE IF NOT EXISTS flightproject;
USE flightproject;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    name VARCHAR(50) PRIMARY KEY,
    password INT NOT NULL
);

-- Job table
CREATE TABLE IF NOT EXISTS job (
    job_id INT PRIMARY KEY,
    job_title VARCHAR(50) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);

-- Employee table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    job_id INT,
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

-- Employee password table
CREATE TABLE IF NOT EXISTS employeepass (
    name VARCHAR(50) PRIMARY KEY,
    password INT NOT NULL
);

-- Airports table
CREATE TABLE IF NOT EXISTS airports (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    terminals INT NOT NULL
);

-- Flight table
CREATE TABLE IF NOT EXISTS flights (
    flightseries VARCHAR(10) NOT NULL,
    flightnumber INT NOT NULL,
    departure VARCHAR(50) NOT NULL,
    arrival VARCHAR(50) NOT NULL,
    departuretime DATETIME NOT NULL,
    arrivaltime DATETIME NOT NULL,
    totalseats INT NOT NULL,
    available INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    distance INT,
    duration INT,
    stops INT,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (flightseries, flightnumber)
);

-- Passenger accounts table
CREATE TABLE IF NOT EXISTS passenger_accounts (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(64) NOT NULL,  -- For storing hashed passwords
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_series VARCHAR(10) NOT NULL,
    flight_number INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (flight_series, flight_number) 
        REFERENCES flights(flightseries, flightnumber)
        ON DELETE CASCADE,
    UNIQUE KEY unique_seat (flight_series, flight_number, seat_number)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id VARCHAR(8) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    flight_series VARCHAR(10) NOT NULL,
    flight_number INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    booking_date DATETIME NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    FOREIGN KEY (username) 
        REFERENCES passenger_accounts(username)
        ON DELETE CASCADE,
    FOREIGN KEY (flight_series, flight_number) 
        REFERENCES flights(flightseries, flightnumber)
        ON DELETE CASCADE,
    FOREIGN KEY (flight_series, flight_number, seat_number) 
        REFERENCES seats(flight_series, flight_number, seat_number)
        ON DELETE CASCADE
);

-- Passenger table (for historical records)
CREATE TABLE IF NOT EXISTS passenger (
    flightserial VARCHAR(10) NOT NULL,
    flightnumber INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    passportserial VARCHAR(10) NOT NULL,
    passportnumber INT NOT NULL,
    dob DATE NOT NULL,
    passportdoi DATE NOT NULL,
    passportdoe DATE NOT NULL,
    visano INT NOT NULL,
    PRIMARY KEY (passportserial, passportnumber),
    FOREIGN KEY (flightserial, flightnumber) 
        REFERENCES flights(flightseries, flightnumber)
        ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_booking_username ON bookings(username);
CREATE INDEX idx_booking_flight ON bookings(flight_series, flight_number);
CREATE INDEX idx_booking_status ON bookings(status);
CREATE INDEX idx_seat_availability ON seats(flight_series, flight_number, is_available);
CREATE INDEX idx_flight_dates ON flights(departuretime, arrivaltime);
CREATE INDEX idx_passenger_flight ON passenger(flightserial, flightnumber);

-- Insert default admin account
INSERT INTO admin (name, password) VALUES ('admin', 1234);

-- Insert some example jobs for test
INSERT INTO job (job_id, job_title, salary) VALUES 
(1, 'Manager', 5000.00),
(2, 'Sales Representative', 3000.00),
(3, 'Customer Service', 2500.00),
(4, 'Pilot', 8000.00),
(5, 'Flight Attendant', 3500.00);

-- Insert example employee for test
INSERT INTO employees (name, position, department, job_id) VALUES 
('John Doe', 'Manager', 'Operations', 1),
('Jane Smith', 'Pilot', 'Flight Crew', 4),
('Peter Jones', 'Flight Attendant', 'Flight Crew', 5);

-- Insert example employee password for test
INSERT INTO employeepass (name, password) VALUES 
('John Doe', 1234),
('Jane Smith', 5678),
('Peter Jones', 1122);

-- Insert example airports for test
INSERT INTO airports (code, name, city, country, terminals) VALUES
('JFK', 'John F. Kennedy International Airport', 'New York', 'USA', 6),
('LHR', 'London Heathrow Airport', 'London', 'UK', 4),
('CDG', 'Charles de Gaulle Airport', 'Paris', 'France', 3),
('SFO', 'San Francisco International Airport', 'San Francisco', 'USA', 4);

-- Insert example flight for test for test
INSERT INTO flights (flightseries, flightnumber, departure, arrival, departuretime, arrivaltime, totalseats, available, status, distance, duration, stops, price) VALUES 
('AA', 101, 'JFK', 'LHR', '2024-08-20 10:00:00', '2024-08-20 22:00:00', 150, 148, 'ON TIME', 5540, 420, 0, 500.00),
('BA', 202, 'LHR', 'CDG', '2024-08-21 09:00:00', '2024-08-21 10:15:00', 120, 120, 'ON TIME', 344, 75, 0, 150.00),
('UA', 303, 'SFO', 'JFK', '2024-08-22 14:00:00', '2024-08-22 22:30:00', 200, 200, 'SCHEDULED', 4150, 330, 0, 350.00),
('AF', 404, 'CDG', 'SFO', '2024-08-23 11:00:00', '2024-08-23 14:00:00', 180, 180, 'ON TIME', 8950, 690, 0, 700.00),
('DL', 505, 'JFK', 'SFO', '2024-08-24 08:00:00', '2024-08-24 11:30:00', 160, 158, 'DELAYED', 4150, 360, 0, 320.00),
('LH', 606, 'LHR', 'JFK', '2024-08-25 12:00:00', '2024-08-25 15:00:00', 220, 220, 'CANCELLED', 5540, 450, 0, 480.00);

-- Insert example seats for the flight for test
INSERT INTO seats (flight_series, flight_number, seat_number, is_available) VALUES 
('AA', 101, '1A', TRUE),
('AA', 101, '1B', FALSE),
('AA', 101, '1C', FALSE),
('AA', 101, '2A', TRUE),
('AA', 101, '2B', TRUE),
('AA', 101, '2C', TRUE),
('BA', 202, '1A', TRUE),
('BA', 202, '1B', TRUE),
('UA', 303, '1A', TRUE),
('AF', 404, '1A', TRUE),
('AF', 404, '1B', TRUE),
('DL', 505, '1A', TRUE),
('DL', 505, '1B', FALSE),
('DL', 505, '1C', FALSE),
('LH', 606, '1A', TRUE);

-- Insert example passenger accounts
INSERT INTO passenger_accounts (username, password, email, name, phone, created_at) VALUES
('alice', 'hashed_pw_1', 'alice@example.com', 'Alice Wonderland', '111-222-3333', '2024-01-15 10:30:00'),
('bob', 'hashed_pw_2', 'bob@example.com', 'Bob Builder', '444-555-6666', '2024-02-20 18:00:00');

-- Insert example bookings
INSERT INTO bookings (booking_id, username, flight_series, flight_number, seat_number, booking_date, payment_method, status) VALUES
('BOOK001', 'alice', 'AA', 101, '1B', '2024-07-01 11:00:00', 'Credit Card', 'CONFIRMED'),
('BOOK002', 'bob', 'AA', 101, '1C', '2024-07-02 12:00:00', 'PayPal', 'CONFIRMED');

-- Insert example historical passenger data
INSERT INTO passenger (flightserial, flightnumber, name, passportserial, passportnumber, dob, passportdoi, passportdoe, visano) VALUES
('AA', 101, 'Charlie Bucket', 'USA', 987654, '1995-05-20', '2020-01-01', '2030-01-01', 123456789); 