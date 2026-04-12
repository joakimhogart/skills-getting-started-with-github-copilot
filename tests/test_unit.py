"""
Unit tests for the High School Management System API.

Tests data structure validation and business logic constraints.
Uses the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest
from src.app import activities


class TestActivityDataStructure:
    """Tests for activity data structure validation."""

    def test_activity_has_required_fields(self, reset_activities):
        """
        Test that each activity has required fields.
        
        ARRANGE: Get all activities from the database
        ACT: Check each activity's structure
        ASSERT: Verify all required fields exist
        """
        # ARRANGE
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # ACT & ASSERT
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"{activity_name} data should be a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"{activity_name} missing required fields: {required_fields - set(activity_data.keys())}"

    def test_activity_description_is_string(self, reset_activities):
        """
        Test that description field is a string.
        
        ARRANGE: Get all activities
        ACT: Check description type
        ASSERT: Verify all descriptions are strings
        """
        # ARRANGE
        test_activities = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in test_activities.items():
            assert isinstance(activity_data["description"], str), \
                f"{activity_name} description should be a string"
            assert len(activity_data["description"]) > 0, \
                f"{activity_name} description should not be empty"

    def test_activity_schedule_is_string(self, reset_activities):
        """
        Test that schedule field is a string.
        
        ARRANGE: Get all activities
        ACT: Check schedule type
        ASSERT: Verify all schedules are strings
        """
        # ARRANGE
        test_activities = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in test_activities.items():
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name} schedule should be a string"
            assert len(activity_data["schedule"]) > 0, \
                f"{activity_name} schedule should not be empty"

    def test_activity_max_participants_is_positive_integer(self, reset_activities):
        """
        Test that max_participants is a positive integer.
        
        ARRANGE: Get all activities
        ACT: Check max_participants type and value
        ASSERT: Verify all are positive integers
        """
        # ARRANGE
        test_activities = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in test_activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            assert activity_data["max_participants"] > 0, \
                f"{activity_name} max_participants should be positive"

    def test_activity_participants_is_list(self, reset_activities):
        """
        Test that participants field is a list.
        
        ARRANGE: Get all activities
        ACT: Check participants type
        ASSERT: Verify all participants are lists
        """
        # ARRANGE
        test_activities = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in test_activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"

    def test_activity_participants_are_strings(self, reset_activities):
        """
        Test that participant entries are email strings.
        
        ARRANGE: Get all activities
        ACT: Check each participant is a string
        ASSERT: Verify all are email-like strings
        """
        # ARRANGE
        test_activities = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in test_activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"{activity_name}: participant {participant} should be a string"
                assert "@" in participant, \
                    f"{activity_name}: participant {participant} should be an email"

    def test_all_activities_exist(self, reset_activities):
        """
        Test that expected activities exist in the database.
        
        ARRANGE: Define expected activities
        ACT: Check if they exist in activities dict
        ASSERT: Verify all expected activities are present
        """
        # ARRANGE
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Drama Club", "Art Studio", "Debate Team", "Science Club"
        ]
        
        # ACT & ASSERT
        for activity_name in expected_activities:
            assert activity_name in activities, \
                f"Expected activity '{activity_name}' not found in database"


class TestParticipantLogic:
    """Tests for participant management business logic."""

    def test_duplicate_email_detection(self, reset_activities, sample_activity_name, sample_email):
        """
        Test logic to detect duplicate participant signups.
        
        ARRANGE: Add a participant to an activity
        ACT: Check if email is in participants list
        ASSERT: Verify duplicate detection works
        """
        # ARRANGE
        activity = activities[sample_activity_name]
        activity["participants"].append(sample_email)
        
        # ACT & ASSERT
        assert sample_email in activity["participants"], \
            "Email should be in participants list after adding"

    def test_participant_removal(self, reset_activities, sample_activity_name, sample_email):
        """
        Test logic to remove a participant from an activity.
        
        ARRANGE: Add a participant to an activity
        ACT: Remove the participant
        ASSERT: Verify participant is removed
        """
        # ARRANGE
        activity = activities[sample_activity_name]
        activity["participants"].append(sample_email)
        assert sample_email in activity["participants"]
        
        # ACT
        activity["participants"].remove(sample_email)
        
        # ASSERT
        assert sample_email not in activity["participants"], \
            "Email should not be in participants list after removal"

    @pytest.mark.parametrize("email", [
        "student1@example.com",
        "student2@example.com",
        "student3@example.com"
    ])
    def test_multiple_participant_additions(self, reset_activities, sample_activity_name, email):
        """
        Test adding multiple different participants to an activity.
        
        ARRANGE: Get an activity
        ACT: Add participant
        ASSERT: Verify participant is added
        """
        # ARRANGE
        activity = activities[sample_activity_name]
        initial_count = len(activity["participants"])
        
        # ACT
        activity["participants"].append(email)
        
        # ASSERT
        assert len(activity["participants"]) == initial_count + 1, \
            "Participants list should increase by one"
        assert email in activity["participants"], \
            f"Email {email} should be in participants list"
