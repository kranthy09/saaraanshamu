"""
Tests for User API: Create Token
"""


def test_create_access_token(test_app_with_db):
    """Test '/token' endpoint"""
    response = test_app_with_db.post(
        "/token",
        data={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
