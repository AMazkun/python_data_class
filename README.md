# SQL and Python Data class tests

Python

SQLite

A Python Data class tests for creating, managing, and storing employee records in a SQLite database. 
It supports CRUD operations (Create, Read, Update, Delete) on a SQLite database and includes utilities for generating mock data to simulate real-world scenarios. The project showcases advanced Python concepts like dataclasses, enums, properties, and database integration, making it a robust example of backend development.

Working with SQLite databases for data persistence.
Applying OOP principles and Python best practices.
Handling data validation and transaction logic.

## Features

### Employee Management:

Create and manage Person objects with attributes like name, address, role, balance, emails, and active status.
Support for four roles: Employee, Manager, Senior Manager, and Director using a custom Role enum.

## Database Operations:

Store and retrieve employee data in a SQLite database.

Perform CRUD operations (insert, fetch, update, delete) via the DatabaseController class.
Generate mock employee data for testing.

## Transaction System:

Deposit and withdraw funds from an employee's balance with validation checks.
Ensure data integrity with error handling for invalid transactions.

## Data Conversion:

Convert database rows to Person objects and vice versa for seamless interaction.
Generate unique 12-character IDs for each employee.

## Mock Data Generation:

Create realistic mock Person objects with randomized names, addresses, roles, emails, and balances.
