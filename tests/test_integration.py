"""
Integration tests for the High School Management System API.

Tests full endpoint workflows and API behavior.
Uses the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        ARRANGE: Set up test client
        ACT: Make GET request to /activities
        ASSERT: Verify response contains all activities
        """
        # ARRANGE
        expected_activity_count = 9
        
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200, "Should return 200 OK"
        activities_data = response.json()
        assert isinstance(activities_data, dict), "Response should be a dictionary"
        assert len(activities_data) == expected_activity_count, \
            f"Should return {expected_activity_count} activities"

    def test_get_activities_returns_activity_structure(self, client):
        """
        Test that returned activities have correct structure.
        
        ARRANGE: Set up test client
        ACT: Make GET request and inspect first activity
        ASSERT: Verify activity has required fields
        """
        # ARRANGE
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # ACT
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        for activity_name, activity in activities_data.items():
            assert required_fields.issubset(activity.keys()), \
                f"{activity_name} missing required fields"
            assert isinstance(activity["participants"], list), \
                f"{activity_name} participants should be a list"

    @pytest.mark.parametrize("activity_name", [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Drama Club", "Art Studio", "Debate Team", "Science Club"
    ])
    def test_get_activities_contains_specific_activity(self, client, activity_name):
        """
        Test that specific activities are returned.
        
        ARRANGE: Set up test client with activity name
        ACT: Make GET request and check for activity
        ASSERT: Verify activity exists in response
        """
        # ARRANGE
        # (activity_name passed via parametrize)
        
        # ACT
        response = client.get("/activities")
        activities_data = response.json()
        
        # ASSERT
        assert activity_name in activities_data, \
            f"Activity '{activity_name}' should be in response"


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client, sample_activity_name, sample_email):
        """
        Test successful signup to an activity.
        
        ARRANGE: Set up test data (activity name and email)
        ACT: Make POST request to signup endpoint
        ASSERT: Verify successful signup response and participant added
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = sample_email
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 200, "Should return 200 OK"
        data = response.json()
        assert "message" in data, "Response should contain a message"
        assert email in data["message"], "Message should mention the email"
        assert activity_name in data["message"], "Message should mention the activity"

    def test_signup_adds_participant_to_activity(self, client, sample_activity_name, sample_email):
        """
        Test that signup actually adds participant to activity.
        
        ARRANGE: Set up test data
        ACT: Signup and then retrieve activities
        ASSERT: Verify participant appears in activity's participant list
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = sample_email
        
        # ACT
        client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        response = client.get("/activities")
        
        # ASSERT
        activities_data = response.json()
        assert email in activities_data[activity_name]["participants"], \
            "Email should be added to participants list"

    def test_signup_nonexistent_activity_returns_404(self, client, sample_email, nonexistent_activity_name):
        """
        Test that signing up for nonexistent activity returns 404.
        
        ARRANGE: Set up test data with nonexistent activity
        ACT: Make POST request to signup
        ASSERT: Verify 404 Not Found error
        """
        # ARRANGE
        activity_name = nonexistent_activity_name
        email = sample_email
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 404, "Should return 404 Not Found"
        assert "not found" in response.json()["detail"].lower(), \
            "Error message should mention 'not found'"

    def test_signup_duplicate_email_returns_400(self, client, sample_activity_name):
        """
        Test that duplicate signup returns 400 Bad Request.
        
        ARRANGE: Signup once with an email
        ACT: Try to signup again with the same email
        ASSERT: Verify 400 Bad Request error
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = "duplicate@example.com"
        
        # First signup should succeed
        client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ACT - Try to signup again with same email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 400, "Should return 400 Bad Request"
        assert "already signed up" in response.json()["detail"].lower(), \
            "Error message should mention 'already signed up'"

    def test_signup_same_email_different_activities(self, client, sample_email):
        """
        Test that same email can signup for multiple different activities.
        
        ARRANGE: Set up test email
        ACT: Signup for two different activities
        ASSERT: Verify both signups succeed
        """
        # ARRANGE
        email = sample_email
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # ACT
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"activity_name": activity1, "email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"activity_name": activity2, "email": email}
        )
        
        # ASSERT
        assert response1.status_code == 200, "First signup should succeed"
        assert response2.status_code == 200, "Second signup should succeed"
        
        # Verify both signups were recorded
        response = client.get("/activities")
        activities_data = response.json()
        assert email in activities_data[activity1]["participants"], \
            f"Email should be in {activity1}"
        assert email in activities_data[activity2]["participants"], \
            f"Email should be in {activity2}"

    @pytest.mark.parametrize("email", [
        "student1@example.com",
        "student2@example.com",
        "student3@example.com"
    ])
    def test_signup_multiple_different_students(self, client, sample_activity_name, email):
        """
        Test that multiple different students can signup for same activity.
        
        ARRANGE: Set up activity and different emails
        ACT: Signup multiple students
        ASSERT: Verify all students added to activity
        """
        # ARRANGE
        activity_name = sample_activity_name
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 200, "Signup should succeed"


class TestRemoveParticipant:
    """Tests for the DELETE /activities/{activity_name}/participant endpoint."""

    def test_remove_participant_successful(self, client, sample_activity_name):
        """
        Test successful removal of a participant from an activity.
        
        ARRANGE: Signup a participant, then prepare to remove them
        ACT: Make DELETE request to remove participant
        ASSERT: Verify successful removal response
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = "remove_test@example.com"
        
        # First signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 200, "Should return 200 OK"
        data = response.json()
        assert "message" in data, "Response should contain a message"
        assert email in data["message"], "Message should mention the email"

    def test_remove_participant_removes_from_activity(self, client, sample_activity_name):
        """
        Test that remove participant actually removes from activity.
        
        ARRANGE: Signup a participant
        ACT: Remove participant and check activities
        ASSERT: Verify participant no longer in activity
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = "remove_test2@example.com"
        
        # Signup first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ACT
        client.delete(
            f"/activities/{activity_name}/participant",
            params={"activity_name": activity_name, "email": email}
        )
        response = client.get("/activities")
        
        # ASSERT
        activities_data = response.json()
        assert email not in activities_data[activity_name]["participants"], \
            "Email should be removed from participants list"

    def test_remove_nonexistent_activity_returns_404(self, client, nonexistent_activity_name):
        """
        Test that removing from nonexistent activity returns 404.
        
        ARRANGE: Set up test data with nonexistent activity
        ACT: Make DELETE request
        ASSERT: Verify 404 Not Found error
        """
        # ARRANGE
        activity_name = nonexistent_activity_name
        email = "test@example.com"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 404, "Should return 404 Not Found"
        assert "not found" in response.json()["detail"].lower(), \
            "Error message should mention 'not found'"

    def test_remove_nonexistent_participant_returns_404(self, client, sample_activity_name):
        """
        Test that removing nonexistent participant returns 404.
        
        ARRANGE: Set up activity with email that is not a participant
        ACT: Try to remove non-participant
        ASSERT: Verify 404 Not Found error
        """
        # ARRANGE
        activity_name = sample_activity_name
        email = "nonexistent_participant@example.com"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"activity_name": activity_name, "email": email}
        )
        
        # ASSERT
        assert response.status_code == 404, "Should return 404 Not Found"
        assert "participant not found" in response.json()["detail"].lower(), \
            "Error message should mention 'participant'"

    def test_remove_existing_participant(self, client, sample_activity_name):
        """
        Test removing an existing participant from an activity.
        
        ARRANGE: Get an activity that already has participants
        ACT: Remove one of the existing participants
        ASSERT: Verify they are removed
        """
        # ARRANGE
        activity_name = sample_activity_name
        # Chess Club has "michael@mergington.edu" as a participant
        email_to_remove = "michael@mergington.edu"
        
        # Verify participant exists
        response = client.get("/activities")
        assert email_to_remove in response.json()[activity_name]["participants"], \
            "Participant should exist before removal"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participant",
            params={"activity_name": activity_name, "email": email_to_remove}
        )
        
        # ASSERT
        assert response.status_code == 200, "Removal should succeed"
        
        # Verify participant is removed
        response = client.get("/activities")
        assert email_to_remove not in response.json()[activity_name]["participants"], \
            "Participant should be removed after deletion"

    def test_remove_multiple_participants_sequentially(self, client, sample_activity_name):
        """
        Test removing multiple participants one by one.
        
        ARRANGE: Signup multiple participants
        ACT: Remove each participant sequentially
        ASSERT: Verify each is removed correctly
        """
        # ARRANGE
        activity_name = sample_activity_name
        emails = ["remove1@example.com", "remove2@example.com", "remove3@example.com"]
        
        # Signup all
        for email in emails:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"activity_name": activity_name, "email": email}
            )
        
        # ACT - Remove each one
        for email in emails:
            response = client.delete(
                f"/activities/{activity_name}/participant",
                params={"activity_name": activity_name, "email": email}
            )
            # ASSERT - Each removal should succeed
            assert response.status_code == 200, f"Should remove {email}"
        
        # ASSERT - Verify all are removed
        response = client.get("/activities")
        activities_data = response.json()
        for email in emails:
            assert email not in activities_data[activity_name]["participants"], \
                f"Email {email} should be fully removed"
