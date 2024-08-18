# Course Management API

## Overview

This project is a simple REST API built using FastAPI that manages "Course" records. The API supports operations such as creating, reading, and deleting courses, and ensures that course numbers are formatted correctly and that duplicate courses cannot be created.

### Features

- **Create a Course**: Allows the insertion of a new course with validation to ensure the course number is a three-digit, zero-padded string (e.g., "033").
- **Search Courses**: Search for courses by their description, supporting partial matches.
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

To create a course, send a POST request to `/v1/courses/` with a JSON body:

   ```json
   {
     "subject": "BIO",
     "courseNumber": "101",
     "description": "Introduction to Biology"
   }
   ```

### Searching for a Course
To search for courses by description, send a GET request to /v1/courses/?description=<search_term>:
   ```bash
   GET /v1/courses/?description=Biology 
   ```

### Deleting a Course
To delete a course, send a DELETE request to /v1/courses/{course_id}:
   ```bash
   DELETE /v1/courses/1
   ```

## Testing

To run the test suite, simply use `pytest`:

   ```bash
   pytest
   ```

## Versioning

### v1: Basic Functionality

The current version of the API (v1) includes the basic functionality as described above, such as creating, searching, and deleting courses, along with validation to prevent duplicate entries and ensure correct course number formatting.

### v2: Future Upgrades

In future versions (v2 and beyond), it is likely to introduce more advanced features. Potential upgrades could include:

* **Advanced Search Capabilities**: Enhance the search functionality to include filtering by multiple criteria such as subject, course number, etc.
* **Additional Fields**: Add more fields to the Course model, such as `credits`, `instructor`, or `semester`.
* **Improved Validation**: Include more complex validation rules, such as ensuring that certain fields are unique or meet specific criteria.
* **Batch Operations**: Allow batch creation or deletion of courses to improve efficiency.

These features would be introduced under the `/v2/` endpoint, while maintaining backward compatibility with the `/v1/` endpoint.
