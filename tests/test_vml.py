import pytest

from email_validator import validate_email

from virtmulib.applogic import usecases
from virtmulib.applogic.onloader import SpotifyOnLoader

# def test_login_get_email_spotify() -> bool:
# 	email = usecases.LoginSignup()(SpotifyOnLoader)
# 	assert email is not None
# 	try:
# 		validate_email(email).normalized
# 	except Exception as e:
# 		assert False


def test_get_user_data_spotify() -> bool:
	usecases.GetUserData()(SpotifyOnLoader)
	assert True
