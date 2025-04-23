import pytest

from backend.user_management.domain.models import Email

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
    