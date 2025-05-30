from datetime import datetime

import pytest

from used_codes.user_registration import UserRegistration


# Fixtures for testing
@pytest.fixture
def registration_instance():
    """Fixture providing a fresh UserRegistration instance for each test."""
    return UserRegistration()

@pytest.fixture
def valid_user_data():
    """Fixture providing valid user data for registration."""
    return {"username": "testuser123", "password": "ValidPass123"}

@pytest.fixture
def existing_user(registration_instance):
    """Fixture that pre-registers a user for tests needing existing data."""
    user_data = {"username": "existinguser", "password": "Existing123"}
    registration_instance.register_user(**user_data)
    return user_data

# Test cases
class TestUserRegistration:
    """Test cases for UserRegistration class."""
    
    def test_validate_username_valid(self, registration_instance):
        """Test username validation with valid usernames."""
        valid_usernames = ["user123", "USER456", "validUser", "123456"]
        for username in valid_usernames:
            assert registration_instance.validate_username(username) is True
    
    def test_validate_username_invalid(self, registration_instance):
        """Test username validation with invalid usernames."""
        invalid_usernames = ["", "usr", "thisusernameistoolongtobevalid", "invalid@user", "user name"]
        for username in invalid_usernames:
            assert registration_instance.validate_username(username) is False
    
    def test_validate_password_valid(self, registration_instance):
        """Test password validation with valid passwords."""
        valid_passwords = ["ValidPass123", "Another1Pass", "1StrongPASS"]
        for password in valid_passwords:
            assert registration_instance.validate_password(password) is True
    
    def test_validate_password_invalid(self, registration_instance):
        """Test password validation with invalid passwords."""
        invalid_passwords = ["", "short", "alllowercase", "ALLUPPERCASE", "12345678", "NoDigitsHere"]
        for password in invalid_passwords:
            assert registration_instance.validate_password(password) is False
    
    def test_register_user_success(self, registration_instance, valid_user_data):
        """Test successful user registration."""
        result = registration_instance.register_user(**valid_user_data)
        assert result["status"] == "success"
        assert valid_user_data["username"] in registration_instance.registered_users
    
    def test_register_user_existing(self, registration_instance, existing_user):
        """Test registration with existing username."""
        result = registration_instance.register_user(**existing_user)
        assert result["status"] == "error"
        assert "already exists" in result["message"]
    
    def test_register_user_invalid_username(self, registration_instance):
        """Test registration with invalid username."""
        invalid_data = {"username": "bad@user", "password": "ValidPass123"}
        result = registration_instance.register_user(**invalid_data)
        assert result["status"] == "error"
        assert "username" in result["message"].lower()
    
    def test_register_user_invalid_password(self, registration_instance):
        """Test registration with invalid password."""
        invalid_data = {"username": "gooduser", "password": "weak"}
        result = registration_instance.register_user(**invalid_data)
        assert result["status"] == "error"
        assert "password" in result["message"].lower()
    
    def test_registration_date_recorded(self, registration_instance, valid_user_data):
        """Test that registration date is properly recorded."""
        result = registration_instance.register_user(**valid_user_data)
        assert result["status"] == "success"
        user_record = registration_instance.registered_users[valid_user_data["username"]]
        assert "registration_date" in user_record
        # Verify the date is recent (within last minute)
        reg_date = datetime.fromisoformat(user_record["registration_date"])
        assert (datetime.now() - reg_date).total_seconds() < 60