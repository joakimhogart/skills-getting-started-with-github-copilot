"""
Shared pytest configuration and fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the entire test session"""
    return TestClient(app)


@pytest.fixture
def client():
    """Create a fresh test client for each test"""
    return TestClient(app)
