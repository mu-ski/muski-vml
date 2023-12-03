import pytest

from email_validator import validate_email

from virtmulib.applogic import usecases
from virtmulib.applogic.onloader.spotify_onloader import SpotifyOnLoader
from virtmulib.entities import *

# def test_login_get_displayname_spotify() -> bool:
# 	name = usecases.LoginSignup()(SpotifyOnLoader)
# 	assert name is not None and name != ''


def test_get_user_data_spotify() -> User:
	user = usecases.GetUserData()(SpotifyOnLoader)
	assert True


# def test_new_design():
# 	hh = Genre(name='hip hop')
# 	exp = Genre(name='experimental')
# 	yassin = Artist(name='Yasiin Bey', genres=[hh, exp])
# 	trck = Track(name='Quiet Dog Bite Hard', artist=yassin, date=SimpleDate('2011').dt)
# 	trck2 = Track(name='Case Bey', artist=yassin, date=SimpleDate('2011').dt)
# 	albm = Album(name='The Ecstatic', artist=yassin, date=SimpleDate('2011').dt)
	
