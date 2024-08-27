# Course Management API

## Overview

This project is a REST API built using FastAPI to manage "Course" records. The API supports operations such as creating, reading, updating, and deleting courses, while ensuring proper validation, formatting, and prevention of duplicates.

### Features

- **Create a Course**: Allows the insertion of a new course with validation to ensure the course number is a three-digit, zero-padded string (e.g., "033").
- **Search Courses**: Search for courses by their description, supporting partial matches.
- **Pagination**: Fetch courses with pagination support to handle large datasets.
- **Update a Course**: Modify existing course details.
- **Delete a Course**: Removes a course from the database by its ID.
- **Prevent Duplicates**: Ensures that courses with the same subject and course number cannot be duplicated.
- **Automatic Database Creation**: The SQLite database is automatically created when the API starts.

## Getting Started

### Requirements

- Python 3.8+
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- SQLAlchemy
- Pytest

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AlexanderPayanoMiranda/course-management-api

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Start the API:
   ```bash
   uvicorn app.main:app --reload

4. Access the API documentation:

Visit http://127.0.0.1:8000/docs to view the automatically generated API documentation using Swagger UI.

## Usage

### Creating a Course

To create a course, send a POST request to `/v2/courses/` with a JSON body:

   ```json
   {
     "subject": "BIO",
     "courseNumber": "101",
     "description": "Introduction to Biology"
   }
   ```

### Searching for a Course
To search for courses by description or subject, send a GET request to `/v2/courses/`:
   ```bash
   GET /v2/courses/?description=Biology&subject=BIO
   ```

### Pagination
To fetch courses with pagination, send a GET request to `/v2/courses/` with `skip` and `limit` parameters:
   ```bash
   GET /v2/courses/?skip=0&limit=10
   ```

### Updating a Course
To update an existing course, send a PUT request to `/v2/courses/{course_id}` with a JSON body containing the updated data:
   ```json
   {
      "subject": "BIO",
      "courseNumber": "101",
      "description": "Advanced Biology"
   }
   ```

### Deleting a Course
To delete a course, send a DELETE request to `/v2/courses/{course_id}`:
   ```bash
   DELETE /v2/courses/1
   ```

## Testing

To run the test suite, simply use `pytest`:

   ```bash
   pytest
   ```

## Versioning

### v1: Basic Functionality

The old version of the API (v1) includes the basic functionality as described above, such as creating, searching, and deleting courses, along with validation to prevent duplicate entries and ensure correct course number formatting.

### v2: Enhanced Functionality

The current version of the API (v2) introduces several enhancements over v1, including:

* Pagination support for fetching courses.
* An endpoint to update existing courses.
* Improved validation and response codes (e.g., returning 201 Created on successful creation).
* Maintenance of backward compatibility with v1 endpoints.

### Future Upgrades (v3)
In future versions (v3 and beyond), potential upgrades could include:

* Advanced Search Capabilities: Enhance the search functionality to include filtering by multiple criteria, such as course number, credits, instructor, or semester.
* Batch Operations: Support for batch creation, updating, or deletion of courses to improve efficiency.
* Role-based Access Control (RBAC): Introduce user authentication and authorization, allowing different user roles to have varying levels of access and permissions.
* Asynchronous Operations: Optimize performance by introducing asynchronous database operations, especially for handling large datasets.
* Versioning Improvements: Continue improving API versioning strategies to ensure smooth transitions and backward compatibility.

These features would likely be introduced under the /v3/ endpoint, ensuring that the system remains robust and scalable while maintaining compatibility with earlier versions.
