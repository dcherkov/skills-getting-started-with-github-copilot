from src.app import activities


def test_unregister_removes_participant(client):
    email = activities["Chess Club"]["participants"][0]

    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_400_for_missing_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "notregistered@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}
