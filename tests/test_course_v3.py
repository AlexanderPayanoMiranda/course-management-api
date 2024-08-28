from fastapi.testclient import TestClient
from app.main import app
from app.api.v3.database import SessionLocal, Base, engine
from app.api.v3.models import Course
import pytest

client = TestClient(app)


# Fixture for creating the database and cleaning up after tests
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables
    Base.metadata.drop_all(bind=engine)


def test_create_course():
    response = client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
            "credits": 3,
            "instructor": "Dr. Smith",
            "semester": "Fall 2024",
            "capacity": 30,
        },
    )
    assert response.status_code == 201
    assert response.json()["subject"] == "BIO"


def test_create_duplicate_course():
    client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
            "credits": 3,
            "instructor": "Dr. Smith",
            "semester": "Fall 2024",
            "capacity": 30,
        },
    )
    response = client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Advanced Biology",
            "credits": 4,
            "instructor": "Dr. Johnson",
            "semester": "Spring 2025",
            "capacity": 25,
        },
    )
    print(response.json())  # Print response to debug
    assert response.status_code == 400


def test_search_course_by_instructor_and_semester():
    client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
            "credits": 3,
            "instructor": "Dr. Smith",
            "semester": "Fall 2024",
            "capacity": 30,
        },
    )
    response = client.get("/v3/courses/?instructor=Dr. Smith&semester=Fall 2024")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["instructor"] == "Dr. Smith"


def test_batch_create_courses():
    response = client.post(
        "/v3/courses/batch/",
        json=[
            {
                "subject": "BIO",
                "courseNumber": "102",
                "description": "Biology II",
                "credits": 4,
                "instructor": "Dr. Smith",
                "semester": "Spring 2025",
                "capacity": 30,
            },
            {
                "subject": "CHEM",
                "courseNumber": "101",
                "description": "Chemistry I",
                "credits": 3,
                "instructor": "Dr. Adams",
                "semester": "Fall 2024",
                "capacity": 25,
            },
        ],
    )
    assert response.status_code == 201


def test_pagination():
    for i in range(15):
        response = client.post(
            "/v2/courses/",
            json={
                "subject": f"SUB{i}",
                "courseNumber": f"{i:03}",
                "description": f"Course Description {i}",
            },
        )
        assert response.status_code == 201

    response = client.get("/v2/courses/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 10

    response = client.get("/v2/courses/?skip=10&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 5

    # Test a page that doesn't exist (e.g., page 3 with no results)
    response = client.get("/v2/courses/?skip=20&limit=10")
    assert response.status_code == 404


def test_update_course():
    response = client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
            "credits": 3,
            "instructor": "Dr. Smith",
            "semester": "Fall 2024",
            "capacity": 30,
        },
    )
    course_id = response.json().get("id")
    if course_id is None:
        pytest.fail("Failed to create course, no ID returned.")

    update_response = client.put(
        f"/v3/courses/{course_id}",
        json={"description": "Advanced Biology"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Advanced Biology"


def test_delete_course():
    response = client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
            "credits": 3,
            "instructor": "Dr. Smith",
            "semester": "Fall 2024",
            "capacity": 30,
        },
    )
    assert response.status_code == 201
    course_id = response.json().get("id")
    assert course_id is not None, "Failed to create course, no ID returned."

    delete_response = client.delete(f"/v3/courses/{course_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/v3/courses/{course_id}")
    assert get_response.status_code == 404
    assert get_response.json().get("detail") == "Course not found"


def test_delete_multiple_courses():
    # Create courses to delete
    response1 = client.post(
        "/v3/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "102",
            "description": "Biology II",
            "credits": 4,
            "instructor": "Dr. Smith",
            "semester": "Spring 2025",
            "capacity": 30,
        },
    )
    assert response1.status_code == 201
    course_id1 = response1.json().get("id")
    assert course_id1 is not None, "Failed to create course 1, no ID returned."

    response2 = client.post(
        "/v3/courses/",
        json={
            "subject": "CHEM",
            "courseNumber": "101",
            "description": "Chemistry I",
            "credits": 3,
            "instructor": "Dr. Adams",
            "semester": "Fall 2024",
            "capacity": 25,
        },
    )
    assert response2.status_code == 201
    course_id2 = response2.json().get("id")
    assert course_id2 is not None, "Failed to create course 2, no ID returned."

    delete_response = client.request(
        "DELETE",
        "/v3/courses/batch/",
        json={"course_ids": [course_id1, course_id2]},
    )
    assert delete_response.status_code == 200

    # Verify deletion
    get_response1 = client.get(f"/v3/courses/{course_id1}")
    assert get_response1.status_code == 404

    get_response2 = client.get(f"/v3/courses/{course_id2}")
    assert get_response2.status_code == 404
