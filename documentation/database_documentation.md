# Freelancer Project Tracker Database Documentation

## Overview
This database is designed to track projects, clients, tasks, time logs, and invoices for a freelancer. It uses MySQL and includes tables for managing all aspects of freelance project management.

## Database Schema

### Clients Table
Stores information about clients.

| Column | Type | Description |
|--------|------|-------------|
| client_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the client |
| name | VARCHAR(255) | Client's name |
| email | VARCHAR(255) UNIQUE | Client's email address |
| phone | VARCHAR(20) | Client's phone number |
| address | TEXT | Client's address |

### Projects Table
Tracks projects associated with clients.

| Column | Type | Description |
|--------|------|-------------|
| project_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the project |
| client_id | INT (FOREIGN KEY) | Reference to the client |
| name | VARCHAR(255) | Project name |
| description | TEXT | Project description |
| start_date | DATE | Project start date |
| end_date | DATE | Project end date |
| status | ENUM('ongoing', 'completed', 'on_hold') | Project status |

### Tasks Table
Manages tasks within projects.

| Column | Type | Description |
|--------|------|-------------|
| task_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the task |
| project_id | INT (FOREIGN KEY) | Reference to the project |
| name | VARCHAR(255) | Task name |
| description | TEXT | Task description |
| status | ENUM('todo', 'in_progress', 'done') | Task status |
| estimated_hours | DECIMAL(5,2) | Estimated hours for the task |

### TimeLogs Table
Records time spent on tasks.

| Column | Type | Description |
|--------|------|-------------|
| timelog_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the time log |
| task_id | INT (FOREIGN KEY) | Reference to the task |
| date | DATE | Date of the time log |
| hours | DECIMAL(5,2) | Hours worked |
| description | TEXT | Description of the work done |

### Invoices Table
Handles invoicing for projects.

| Column | Type | Description |
|--------|------|-------------|
| invoice_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the invoice |
| project_id | INT (FOREIGN KEY) | Reference to the project |
| client_id | INT (FOREIGN KEY) | Reference to the client |
| amount | DECIMAL(10,2) | Invoice amount |
| date_issued | DATE | Date the invoice was issued |
| due_date | DATE | Invoice due date |
| status | ENUM('unpaid', 'paid', 'overdue') | Invoice status |

## Relationships
- A Client can have multiple Projects.
- A Project belongs to one Client and can have multiple Tasks.
- A Task belongs to one Project and can have multiple TimeLogs.
- An Invoice is linked to one Project and one Client.

## Sample Data
The database includes sample data with 3 entries in each table for testing purposes.

## Usage
To set up the database:
1. Run the SQL script `FreelancerProjectTrakcer.sql` in your MySQL environment.
2. The script creates the database, tables, and inserts sample data.

## Notes
- All foreign keys have CASCADE DELETE to maintain referential integrity.
- Dates are stored in YYYY-MM-DD format.
- Amounts are stored as DECIMAL for precision.