"""
Tests for User API: Create Token
"""


def test_create_access_token(test_app_with_db):
    """Test '/token' endpoint"""
    response = test_app_with_db.post(
        "/token",
        data={"username": "kranthi", "password": "secret"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_unauthorized_user_create_access_token(test_app_with_db):
    """Test unauthorized user"""
    response = test_app_with_db.post(
        "/token",
        data={"username": "unauthorized", "password": "secret"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_users_me_success(test_app_with_db):
    """Test user details success"""

    response = test_app_with_db.post(
        "/token",
        data={"username": "kranthi", "password": "secret"},
    )
    print(response.json())
    access_token = response.json()["access_token"]

    response = test_app_with_db.get(
        "/users/me", headers={"Authorization": f"bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "kranthi"
