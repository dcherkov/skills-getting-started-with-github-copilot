from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_dictionary_payload(client):
    response = client.get("/activities")

    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert payload["Chess Club"]["schedule"] == activities["Chess Club"]["schedule"]
    assert isinstance(payload["Chess Club"]["participants"], list)
