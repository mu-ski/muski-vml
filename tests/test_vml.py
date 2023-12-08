import pytest
from _pytest.monkeypatch import MonkeyPatch
import json
from email_validator import validate_email

from virtmulib.applogic import usecases
from virtmulib.applogic.onload.onload_spotify import OnLoadSpotify, SpotifyAPICall
from virtmulib.entities import *

test_data = json.loads(open("tests/json_test_data/test.json", 'r').read())
monkeypatch = MonkeyPatch()

def _obj_to_dict_items(ls: list[VMLThing]) -> str:
    return json.loads(
            json.dumps(
                {"items": [
                    i.model_dump(exclude_defaults=True) 
                    for i in ls]},
                default=str))

def _obj_to_dict(obj: VMLThing) -> str:
    return json.loads(
            json.dumps(
                obj.model_dump(exclude_defaults=True), default=str))

def _dict_to_tuples(test_data: dict, test_name: str) -> list[tuple]:
    td = test_data.get('all_tests').get(test_name)
    return [tuple(t.values()) for t in td]

@pytest.mark.parametrize("input", _dict_to_tuples(test_data, "get_playlists"))
def test_get_user_data_spotify_playlists(input):
    placeholder_test(
            input,
            usecases.GetUserDataPlaylists(OnLoadSpotify))

@pytest.mark.parametrize("input", _dict_to_tuples(test_data, "get_artists"))
def test_get_user_data_spotify_artists(input):
    placeholder_test(
            input,
            usecases.GetUserDataArtists(OnLoadSpotify))

@pytest.mark.parametrize("input", _dict_to_tuples(test_data, "get_albums"))
def test_get_user_data_spotify_albums(input):
    placeholder_test(
            input,
            usecases.GetUserDataAlbums(OnLoadSpotify))


@pytest.mark.parametrize("input", _dict_to_tuples(test_data, "get_tracks"))
def test_get_user_data_spotify_tracks(input):
    placeholder_test(
            input,
            usecases.GetUserDataTracks(OnLoadSpotify))

@pytest.mark.e2e
def test_live_get_user_data_spotify():
    monkeypatch.undo()
    get_user_data_action = usecases.GetUserData(OnLoadSpotify)
    user = get_user_data_action.execute()
    obj = json.dumps(_obj_to_dict(user))
    # print(obj)
    assert obj != {}

def placeholder_test(input, usecase_action: usecases.OnloaderAction):
    ip = input[0]
    ip.reverse()
    exp_out = input[1]

    def mock_call(func, params, inp):
        return ip.pop()

    monkeypatch.setattr(SpotifyAPICall, "_call", mock_call)
    
    out = _obj_to_dict_items(usecase_action.execute())

    # print(json.dumps(out))
    # print(json.dumps(exp_out))

    assert exp_out == out
