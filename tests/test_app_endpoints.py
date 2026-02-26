import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Save and restore activities state for isolation
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

def test_root_redirects_to_static_index_aaa():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code in (307, 302)
    assert "/static/index.html" in response.headers.get("location", "")

def test_get_activities_returns_all_aaa():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())

def test_signup_successful_aaa():
    # Arrange
    client = TestClient(app)
    activity = next(iter(activities))
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_activity_not_found_aaa():
    # Arrange
    client = TestClient(app)
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/NonexistentActivity/signup?email={email}")
    # Assert
    assert response.status_code == 404

def test_signup_already_signed_up_aaa():
    # Arrange
    client = TestClient(app)
    activity = next(iter(activities))
    email = "already@mergington.edu"
    activities[activity]["participants"].append(email)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
