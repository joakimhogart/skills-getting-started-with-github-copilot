"""
Tests for the High School Management System API

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and conditions
- Act: Perform the action being tested
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestRoot:
    def test_root_redirects_to_static(self, client):
        """Test that the root endpoint redirects to /static/index.html"""
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivities:
    def test_get_activities(self, client):
        """Test getting all activities returns expected structure"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        expected_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name in expected_activities:
            assert activity_name in data
            activity = data[activity_name]
            for field in expected_fields:
                assert field in activity
            assert isinstance(activity["participants"], list)

    def test_get_activities_has_existing_participants(self, client):
        """Test that activities have expected participant data"""
        # Arrange
        expected_participants = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, expected_count in expected_participants.items():
            assert len(data[activity_name]["participants"]) == expected_count
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]
        assert "john@mergington.edu" in data["Gym Class"]["participants"]


class TestSignup:
    def test_signup_for_existing_activity(self, client):
        """Test successfully signing up a student for an existing activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that a signup request actually adds the participant"""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        response_before = client.get("/activities")
        initial_count = len(response_before.json()[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        response_after = client.get("/activities")
        final_count = len(response_after.json()[activity_name]["participants"])
        assert final_count == initial_count + 1
        assert email in response_after.json()[activity_name]["participants"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test that signup fails with 404 for a non-existent activity"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_multiple_times_allowed(self, client):
        """Test that a student can sign up multiple times (no duplicate prevention)"""
        # Arrange
        activity_name = "Gym Class"
        email = "test@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        assert participants.count(email) == 2
