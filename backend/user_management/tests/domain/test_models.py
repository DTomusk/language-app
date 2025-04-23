import pytest

from backend.user_management.domain.models import Email, User

def test_valid_emails():
    valid_emails = [
        "test@example.com",
        "user.name+tag+sorting@example.com",
        "user_name@example.co.uk",
        "user-name@sub.example.org",
        "user123@domain123.com"
    ]

    for email in valid_emails:
        try:
            result = Email(email=email)
            assert result.email == email, f"Expected {email}, got {result.email}"
        except ValueError:
            pytest.fail(f"Valid email '{email}' raised ValueError unexpectedly.")
    
def test_invalid_emails():
    invalid_emails = [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@com",
        "username@domain..com",
        "user..@example.com",
    ]

    for email in invalid_emails:
        with pytest.raises(ValueError, match=r"Invalid email format"):
            Email(email=email)

def test_user_creation():
    email = Email(email="mail@e.com")
    hashed_password = "hashed_password"
    user = User(email=email, hashed_password=hashed_password)
    assert user.id is not None, "User ID should be generated"
    assert user.email == email, "User email should match the provided email"
    assert user.hashed_password == hashed_password, "User hashed password should match the provided password"
    