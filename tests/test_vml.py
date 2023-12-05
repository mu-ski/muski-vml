
import pytest
from _pytest.monkeypatch import MonkeyPatch
import json
from email_validator import validate_email

from virtmulib.applogic import usecases
from virtmulib.applogic.onloader.spotify_onloader import SpotifyOnLoader
from virtmulib.entities import *


# test_data = json.loads(open("tests/json_test_data/test.json", 'r').read())
# monkeypatch = MonkeyPatch()

def _dump_obj_list(ls: list[VMLThing]) -> str:
	"""Used for testing"""
	return json.dumps({"items": [i.model_dump(exclude_defaults=True) for i in ls]}, default=str)

def _dump_obj(obj: VMLThing) -> str:
	"""Used for testing"""
	return json.dumps(obj.model_dump(exclude_defaults=True), default=str)


# @pytest.mark.parametrize("input", test_data['all_tests']['get_playlists'])
# def test_get_user_data_spotify_playlists(input):
# 	print(input)
# 	def mockreturn(func, params, inp):
# 		print(func, params, inp)
# 		print(input)
# 		return 
# 	monkeypatch.setattr(SpotifyOnLoader, "call", mockreturn)

# 	output = usecases.GetUserDataPlaylists()(SpotifyOnLoader)





# def test_login_get_displayname_spotify() -> bool:
# 	name = usecases.LoginSignup()(SpotifyOnLoader)
# 	assert name is not None and name != ''

def test_get_user_data_spotify() -> User:
	user = usecases.GetUserData()(SpotifyOnLoader)
	print(_dump_obj(user))
	assert True


