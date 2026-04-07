from src.app import activities


def test_signup_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_email(client):
    duplicate_email = activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess%20Club/signup", params={"email": duplicate_email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_returns_400_when_activity_is_full(client):
    activities["Chess Club"]["participants"] = [
        f"student{i}@mergington.edu"
        for i in range(activities["Chess Club"]["max_participants"])
    ]

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
