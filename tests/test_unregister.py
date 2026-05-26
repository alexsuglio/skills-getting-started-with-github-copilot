def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()
    after = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert len(after) == len(before) - 1
    assert email not in after


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"
