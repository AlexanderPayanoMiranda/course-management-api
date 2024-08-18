from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.database import SessionLocal, Base, engine
from app.api.v1.models import Course
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
        "/v1/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    assert response.status_code == 200
    assert response.json()["subject"] == "BIO"


def test_create_duplicate_course():
    client.post(
        "/v1/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    response = client.post(
        "/v1/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Advanced Biology",
        },
    )
    assert response.status_code == 400


def test_search_course():
    client.post(
        "/v1/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    response = client.get("/v1/courses/?description=Biology")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Introduction to Biology"


def test_delete_course():
    response = client.post(
        "/v1/courses/",
        json={
            "subject": "BIO",
            "courseNumber": "101",
            "description": "Introduction to Biology",
        },
    )
    course_id = response.json()["id"]
    delete_response = client.delete(f"/v1/courses/{course_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/v1/courses/?description=Biology")
    assert get_response.status_code == 404
