-- Create the database
CREATE DATABASE recycling_lives;
USE recycling_lives;

-- Users table (common fields for all user types)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL UNIQUE,
    role ENUM('NGO', 'Restaurant', 'Caterer') NOT NULL,
    region VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zipcode VARCHAR(10),
    particular_mark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- User statistics table
CREATE TABLE user_statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    people_fed INT DEFAULT 0,
    deliveries_done INT DEFAULT 0,
    failed_deliveries INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Food donations table
CREATE TABLE donations (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    quantity INT NOT NULL COMMENT 'Number of people that can be fed',
    food_type VARCHAR(100) NOT NULL,
    cooked_time TIME NOT NULL,
    expiry_hours INT NOT NULL COMMENT 'Hours until expiry',
    hygiene_rating INT NOT NULL CHECK (hygiene_rating BETWEEN 1 AND 5),
    status ENUM('Available', 'Claimed', 'In Delivery', 'Delivered', 'Expired') DEFAULT 'Available',
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zipcode VARCHAR(10),
    particular_mark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Delivery requests table
CREATE TABLE delivery_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    ngo_id INT NOT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected', 'In Progress', 'Completed', 'Failed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (donation_id) REFERENCES donations(donation_id) ON DELETE CASCADE,
    FOREIGN KEY (ngo_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- Delivery history table
CREATE TABLE delivery_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    status ENUM('In Progress', 'Completed', 'Failed') NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES delivery_requests(request_id) ON DELETE CASCADE
);