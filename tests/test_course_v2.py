from fastapi.testclient import TestClient
from app.main import app
from app.api.v2.database import SessionLocal, Base, engine
from app.api.v2.models import Course
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
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    assert response.status_code == 201
    assert response.json()["subject"] == "BIO"


def test_create_duplicate_course():
    client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    response = client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Advanced Biology",
        },
    )
    assert response.status_code == 400


def test_search_course_by_description():
    client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    response = client.get("/v2/courses/?description=Biology")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Introduction to Biology"


def test_search_course_by_subject_and_description():
    client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    response = client.get("/v2/courses/?description=Biology&subject=BIO")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["subject"] == "BIO"
    assert response.json()[0]["description"] == "Introduction to Biology"

    # Test with a different subject
    response = client.get("/v2/courses/?description=Biology&subject=CHEM")
    assert response.status_code == 404


def test_pagination():
    # First, create enough courses to test pagination
    for i in range(15):  # assuming your pagination size is set to 10
        response = client.post(
            "/v2/courses/",
            json={
                "subject": f"SUB{i}",
                "courseNumber": f"{i:03}",
                "description": f"Course Description {i}",
            },
        )
        assert response.status_code == 201  # Created

    # Test the first page of results
    response = client.get("/v2/courses/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 10

    # Test the second page of results
    response = client.get("/v2/courses/?skip=10&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 5  # Remaining courses should be 5

    # Test a page that doesn't exist (e.g., page 3 with no results)
    response = client.get("/v2/courses/?skip=20&limit=10")
    assert response.status_code == 404  # Assuming your API returns 404 when no results


def test_update_course():
    response = client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    course_id = response.json()["id"]

    update_response = client.put(
        f"/v2/courses/{course_id}",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Advanced Biology",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Advanced Biology"

    # Ensure the course is updated
    get_response = client.get(f"/v2/courses/?description=Advanced Biology")
    assert get_response.status_code == 200
    assert get_response.json()[0]["description"] == "Advanced Biology"


def test_delete_course():
    response = client.post(
        "/v2/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    course_id = response.json()["id"]
    delete_response = client.delete(f"/v2/courses/{course_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/v2/courses/?description=Biology")
    assert get_response.status_code == 404
