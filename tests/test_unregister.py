"""
Tests for the unregister endpoint following the AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""

    def test_unregister_successful(self, client, reset_activities):
        """Test successful unregistration from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert f"Unregistered {email} from {activity_name}" in response.json()["message"]

    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister correctly removes the participant from the activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response = client.get("/activities")

        # Assert
        activities_data = response.json()
        assert email not in activities_data[activity_name]["participants"]

    def test_unregister_nonexistent_activity_fails(self, client, reset_activities):
        """Test that unregistering from non-existent activity fails."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_nonexistent_participant_fails(self, client, reset_activities):
        """Test that unregistering non-existent participant fails."""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_unregister_from_activity_with_no_participants_fails(self, client, reset_activities):
        """Test that unregistering from activity with no participants fails gracefully."""
        # Arrange
        activity_name = "Tennis Club"  # Has no participants initially
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_unregister_then_signup_again_succeeds(self, client, reset_activities):
        """Test that a student can sign up again after unregistering."""
        # Arrange
        activity_name = "Tennis Club"
        email = "student@mergington.edu"

        # Act - Sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Act - Unregister
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        # Act - Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert f"Signed up {email} for {activity_name}" in response.json()["message"]