-- Freelancer Project Tracker Database
-- MySQL Script

-- Create the database
CREATE DATABASE IF NOT EXISTS FreelancerProjectTracker;
USE FreelancerProjectTracker;

-- Create Clients table
CREATE TABLE IF NOT EXISTS Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

-- Create Projects table
CREATE TABLE IF NOT EXISTS Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('ongoing', 'completed', 'on_hold') DEFAULT 'ongoing',
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Create Tasks table
CREATE TABLE IF NOT EXISTS Tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('todo', 'in_progress', 'done') DEFAULT 'todo',
    estimated_hours DECIMAL(5,2),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
);

-- Create TimeLogs table
CREATE TABLE IF NOT EXISTS TimeLogs (
    timelog_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    date DATE NOT NULL,
    hours DECIMAL(5,2) NOT NULL,
    description TEXT,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id) ON DELETE CASCADE
);

-- Create Invoices table
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    client_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date_issued DATE NOT NULL,
    due_date DATE,
    status ENUM('unpaid', 'paid', 'overdue') DEFAULT 'unpaid',
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Sample Data Inserts (3 entries as requested)

-- Insert Clients
INSERT INTO Clients (name, email, phone, address) VALUES
('ABC Corp', 'contact@abc.com', '123-456-7890', '123 Main St, City, State'),
('XYZ Ltd', 'info@xyz.com', '987-654-3210', '456 Elm St, City, State'),
('Tech Solutions', 'hello@techsol.com', '555-123-4567', '789 Oak St, City, State');

-- Insert Projects
INSERT INTO Projects (client_id, name, description, start_date, end_date, status) VALUES
(1, 'Website Redesign', 'Redesign company website', '2023-01-01', '2023-03-01', 'completed'),
(2, 'Mobile App Development', 'Develop mobile app for client', '2023-02-01', NULL, 'ongoing'),
(3, 'SEO Optimization', 'Optimize website for search engines', '2023-03-01', '2023-04-01', 'completed');

-- Insert Tasks
INSERT INTO Tasks (project_id, name, description, status, estimated_hours) VALUES
(1, 'Design Mockups', 'Create design mockups', 'done', 20.00),
(2, 'Backend Development', 'Develop backend API', 'in_progress', 40.00),
(3, 'Keyword Research', 'Research keywords', 'done', 10.00);

-- Insert TimeLogs
INSERT INTO TimeLogs (task_id, date, hours, description) VALUES
(1, '2023-01-15', 8.00, 'Worked on initial designs'),
(2, '2023-02-10', 6.50, 'Set up database schema'),
(3, '2023-03-05', 4.00, 'Analyzed competitor keywords');

-- Insert Invoices
INSERT INTO Invoices (project_id, client_id, amount, date_issued, due_date, status) VALUES
(1, 1, 5000.00, '2023-03-01', '2023-03-15', 'paid'),
(2, 2, 8000.00, '2023-04-01', '2023-04-15', 'unpaid'),
(3, 3, 2000.00, '2023-04-01', '2023-04-15', 'paid');