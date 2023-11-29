import pytest
from email_validator import validate_email

from virtmulib.usecases import login_signup
from virtmulib.onloaders import OnLoaderEnum, OnLoader

def test_login_get_email_spotify() -> bool:
	email = login_signup(OnLoaderEnum.spotify)
	valid = None
	try:
		valid = validate_email(email).normalized
	except Exception:
		pass

	assert valid is not None
	
#def test_login_get_email_spotify_fails() -> bool:
#	email = login_signup(OnLoaderEnum.spotify)
# 	assert email is None
