"""
Tests for the signup endpoint following the AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_successful(self, client, reset_activities):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Tennis Club"
        email = "new_student@mergington.edu"
        initial_participant_count = 0

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert f"Signed up {email} for {activity_name}" in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that signup correctly adds the participant to the activity."""
        # Arrange
        activity_name = "Tennis Club"
        email = "new_student@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")

        # Assert
        activities_data = response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_signup_duplicate_fails(self, client, reset_activities):
        """Test that signing up twice fails with appropriate error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """Test that signing up for non-existent activity fails."""
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
        assert "Activity not found" in response.json()["detail"]

    def test_signup_multiple_students_increases_count(self, client, reset_activities):
        """Test that multiple signups correctly increase participant count."""
        # Arrange
        activity_name = "Tennis Club"
        students = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

        # Act
        for email in students:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
        response = client.get("/activities")

        # Assert
        activities_data = response.json()
        assert len(activities_data[activity_name]["participants"]) == len(students)
        for email in students:
            assert email in activities_data[activity_name]["participants"]

    def test_signup_different_activities_independent(self, client, reset_activities):
        """Test that signups for different activities are independent."""
        # Arrange
        email = "student@mergington.edu"
        activity1 = "Tennis Club"
        activity2 = "Art Studio"

        # Act
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})
        response = client.get("/activities")

        # Assert
        activities_data = response.json()
        assert email in activities_data[activity1]["participants"]
        assert email in activities_data[activity2]["participants"]

    def test_signup_activity_at_capacity_fails(self, client, reset_activities):
        """Test that signing up for a full activity fails."""
        # Arrange
        activity_name = "Robotics Club"  # Has max_participants: 14, currently 2 participants
        # Fill the activity to capacity
        for i in range(12):  # Add 12 more to reach 14 total
            email = f"student{i}@mergington.edu"
            client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act - Try to add one more
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "extra_student@mergington.edu"}
        )

        # Assert
        assert response.status_code == 400
        assert "at full capacity" in response.json()["detail"]