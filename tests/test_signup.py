def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()
    after = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert len(after) == len(before) + 1
    assert email in after


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up"


def test_signup_rejects_invalid_email_input(client):
    # Arrange
    activity_name = "Chess Club"
    email = '"><script>alert(1)</script>'

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    after = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 422
    assert email not in after
