"""
Tests for the activities endpoint following the AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client, reset_activities):
        """Test that getting activities returns a successful response with all activities."""
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count
        assert "Chess Club" in response.json()

    def test_get_activities_returns_activity_details(self, client, reset_activities):
        """Test that activities response contains complete activity details."""
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert activity_name in activities_data
        assert "description" in activities_data[activity_name]
        assert "schedule" in activities_data[activity_name]
        assert "max_participants" in activities_data[activity_name]
        assert "participants" in activities_data[activity_name]

    def test_get_activities_contains_correct_participant_count(self, client, reset_activities):
        """Test that activities show correct participant counts."""
        # Arrange
        expected_chess_club_participants = 2

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert len(activities_data["Chess Club"]["participants"]) == expected_chess_club_participants

    def test_get_activities_shows_empty_activity(self, client, reset_activities):
        """Test that activities with no participants are displayed correctly."""
        # Arrange
        empty_activity = "Tennis Club"

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert empty_activity in activities_data
        assert len(activities_data[empty_activity]["participants"]) == 0

    def test_root_redirects_to_static_index(self, client):
        """Test that root path redirects to static/index.html."""
        # Arrange
        redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == redirect_url