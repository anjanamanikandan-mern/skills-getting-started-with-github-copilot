import pytest

# Arrange-Act-Assert pattern is used in all tests

def test_root_redirect(client):
    # Arrange
    # (No special setup needed)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307  # Redirect or OK
    assert "text/html" in response.headers.get("content-type", "")


def test_get_activities(client):
    # Arrange
    # (No special setup needed)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_for_activity_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.delete(f"/activities/{activity}/signup", params={"email": email})
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found(client):
    # Arrange
    activity = "NonExistentClub"
    email = "testuser3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser4@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_remove_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
