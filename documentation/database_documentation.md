# Freelancer Project Tracker Database Documentation

## Overview
This database is designed to track projects, clients, tasks, time logs, and invoices for a freelancer. It uses MySQL and includes tables for managing all aspects of freelance project management. The database ensures data integrity through foreign key constraints and supports cascading deletes.

## ER Diagram
For a visual representation of the database structure and relationships, refer to the ER Diagram in the [Diagrams/ER_Diagram.md](Diagrams/ER_Diagram.md) file.

## Database Schema

### Data Types Explanation
Before diving into the tables, here's an explanation of the data types used:
- **INT**: A 32-bit integer type. Used for IDs and counts. When marked as AUTO_INCREMENT, it automatically assigns a unique number starting from 1 for new rows. PRIMARY KEY indicates it's the unique identifier for the table.
- **VARCHAR(n)**: A variable-length string that can hold up to n characters. Efficient for names and short texts.
- **TEXT**: A large text field for storing longer descriptions or notes, up to 65,535 characters.
- **DATE**: Stores dates in the format YYYY-MM-DD (e.g., '2023-01-15'). Does not include time.
- **DECIMAL(p,s)**: A precise decimal number with p total digits and s digits after the decimal point. Used for monetary values and hours to avoid floating-point precision issues.
- **ENUM**: An enumeration type that restricts values to a predefined list (e.g., 'ongoing', 'completed').

### Clients Table
Stores information about clients. This is the root entity in the hierarchy.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| client_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the client | Primary Key, Auto-increment |
| name | VARCHAR(255) | Client's full name or company name | Not Null |
| email | VARCHAR(255) UNIQUE | Client's email address for communication | Not Null, Unique |
| phone | VARCHAR(20) | Client's phone number | Optional |
| address | TEXT | Client's physical or mailing address | Optional |

### Projects Table
Tracks projects associated with clients. Each project belongs to exactly one client but a client can have multiple projects (one-to-many relationship).

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| project_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the project | Primary Key, Auto-increment |
| client_id | INT (FOREIGN KEY) | Reference to the client who owns the project | Not Null, Foreign Key to Clients.client_id |
| name | VARCHAR(255) | Project name or title | Not Null |
| description | TEXT | Detailed description of the project scope | Optional |
| start_date | DATE | Date when the project began | Optional |
| end_date | DATE | Date when the project was completed | Optional |
| status | ENUM('ongoing', 'completed', 'on_hold') | Current status of the project | Default 'ongoing' |

### Tasks Table
Manages tasks within projects. Tasks are sub-components of projects, allowing breakdown of work (one-to-many from Projects to Tasks).

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| task_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the task | Primary Key, Auto-increment |
| project_id | INT (FOREIGN KEY) | Reference to the project this task belongs to | Not Null, Foreign Key to Projects.project_id |
| name | VARCHAR(255) | Task name or title | Not Null |
| description | TEXT | Detailed description of the task | Optional |
| status | ENUM('todo', 'in_progress', 'done') | Current status of the task | Default 'todo' |
| estimated_hours | DECIMAL(5,2) | Estimated time required to complete the task | Optional |

### TimeLogs Table
Records time spent on tasks. Allows tracking of actual work hours against tasks (one-to-many from Tasks to TimeLogs).

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| timelog_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the time log entry | Primary Key, Auto-increment |
| task_id | INT (FOREIGN KEY) | Reference to the task being worked on | Not Null, Foreign Key to Tasks.task_id |
| date | DATE | Date when the work was performed | Not Null |
| hours | DECIMAL(5,2) | Number of hours worked on that date | Not Null |
| description | TEXT | Description of the work done | Optional |

### Invoices Table
Handles invoicing for projects. Links projects and clients for billing purposes. Note: client_id is included for direct reference, though it's redundant with project_id.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| invoice_id | INT (AUTO_INCREMENT, PRIMARY KEY) | Unique identifier for the invoice | Primary Key, Auto-increment |
| project_id | INT (FOREIGN KEY) | Reference to the project being invoiced | Not Null, Foreign Key to Projects.project_id |
| client_id | INT (FOREIGN KEY) | Reference to the client being invoiced | Not Null, Foreign Key to Clients.client_id |
| amount | DECIMAL(10,2) | Total amount due on the invoice | Not Null |
| date_issued | DATE | Date the invoice was created and sent | Not Null |
| due_date | DATE | Date by which payment is expected | Optional |
| status | ENUM('unpaid', 'paid', 'overdue') | Payment status of the invoice | Default 'unpaid' |

## Relationships
The database uses foreign key constraints to maintain referential integrity. Here's a detailed explanation of the relationships:

- **Clients to Projects**: One-to-Many. One client can have multiple projects, but each project belongs to exactly one client. Deleting a client cascades to delete all their projects.
- **Projects to Tasks**: One-to-Many. A project can contain multiple tasks, but each task belongs to one project. Deleting a project removes all its tasks.
- **Tasks to TimeLogs**: One-to-Many. Multiple time log entries can be associated with a single task, but each log entry is for one task. Deleting a task removes all its time logs.
- **Projects to Invoices**: One-to-Many. A project can have multiple invoices (e.g., partial payments), but each invoice is for one project.
- **Clients to Invoices**: One-to-Many. A client can receive multiple invoices, but each invoice goes to one client. (Note: This relationship is somewhat redundant due to the project link, but allows direct client-invoice queries.)

All foreign keys are set with CASCADE DELETE, meaning deleting a parent record automatically removes related child records to prevent orphaned data.

## Sample Data
The database includes sample data with 3 entries in each table for testing purposes. This allows you to explore the relationships and query examples.

## Usage
To set up the database:
1. Ensure MySQL is installed and running.
2. Run the SQL script `DATABASES/FreelancerProjectTrakcer.sql` in your MySQL environment (e.g., `mysql -u root -p < FreelancerProjectTrakcer.sql`).
3. The script creates the database, tables, and inserts sample data.

## Notes
- All foreign keys have CASCADE DELETE to maintain referential integrity and prevent orphaned records.
- Dates are stored in YYYY-MM-DD format and should be handled accordingly in applications.
- Amounts and hours use DECIMAL for precision; avoid using FLOAT for financial calculations.
- ENUM values are case-sensitive and must match exactly.
- Consider adding indexes on frequently queried columns (e.g., status fields) for performance in larger datasets.