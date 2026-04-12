"""
Shared fixtures and configuration for all tests.

Provides:
- TestClient for FastAPI app
- Clean activities state reset for each test
- Sample test data
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """
    Reset activities to clean state before test.
    
    Use this fixture in unit tests that directly access the activities dictionary.
    """
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for varsity and JV levels",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Wednesdays and Saturdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jordan@mergington.edu", "casey@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theatre productions and performance art",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["laura@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, sculpture, and mixed media projects",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science fair preparation",
            "schedule": "Wednesdays and Saturdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
        }
    })


@pytest.fixture
def client(reset_activities):
    """
    Provide a TestClient for the FastAPI app with fresh activities state.
    
    Resets the activities dictionary to its initial state before each test
    to prevent test pollution.
    """
    # ARRANGE: Reset activities to clean state before test (handled by reset_activities fixture)
    
    # Return TestClient with the app
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provide a sample email for testing."""
    return "test_student@example.com"


@pytest.fixture
def sample_activity_name():
    """Provide a sample activity name that exists in the database."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity_name():
    """Provide an activity name that does not exist in the database."""
    return "Nonexistent Activity"
