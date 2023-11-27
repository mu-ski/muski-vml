import pytest
from email_validator import validate_email

from muskivml.logic import OnLoader

def test_login_get_email() -> bool:
	email = OnLoader.login_with_spotify()
	valid = None
	try:
		valid = validate_email(email).email
	except Exception:
		pass

	assert valid is not None