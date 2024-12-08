# Library Management System API

This is a simple Flask API for managing books and members in a library.

## Features
1. CRUD operations for books and members.
2. Search functionality for books by title or author.
3. Pagination for book listings.
4. Token-based authentication.

## Requirements
- Python 3.x

## How to Run
1. Clone the repository.
2. Run `python app.py`.
3. Use tools like `curl` or Postman to interact with the API.

## Design Choices
- SQLite is used as a lightweight database for simplicity.
- Token-based authentication is implemented directly without third-party libraries.
- Pagination is handled manually using query parameters.

## Assumptions and Limitations
- The token is hardcoded for simplicity.
- Only books and members are implemented; borrowing functionality is not included.
