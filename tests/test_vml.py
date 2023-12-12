import json
import pytest
from _pytest.monkeypatch import MonkeyPatch

import virtmulib.applogic.gateway as usecases
from virtmulib.applogic.onload.spotify import SpotifyAPICall, OnLoadSpotify
from tests.utils import *

test_data = json.loads(open("tests/json_test_data/test.json", "r").read())
monkeypatch = MonkeyPatch()


@pytest.mark.e2e
def test_live_get_user_data_spotify():
    # monkeypatch.undo()
    user = usecases.get_user_data(OnLoadSpotify)
    print(
        len(user.lib_extended.artists),
        len(user.lib_extended.albums),
        len(user.lib_extended.tracks),
        len(user.lib_extended.playlists))
    obj = json.dumps(obj_to_dict(user))
    #print(obj)
    assert obj != {}



@pytest.mark.parametrize("input", dict_to_tuples(test_data, "get_playlists"))
def test_get_user_data_spotify_playlists(input):
    placeholder_test(input, usecases.get_user_playlists, OnLoadSpotify)


@pytest.mark.parametrize("input", dict_to_tuples(test_data, "get_artists"))
def test_get_user_data_spotify_artists(input):
    placeholder_test(input, usecases.get_user_artists, OnLoadSpotify)


@pytest.mark.parametrize("input", dict_to_tuples(test_data, "get_albums"))
def test_get_user_data_spotify_albums(input):
    placeholder_test(input, usecases.get_user_albums, OnLoadSpotify)


@pytest.mark.parametrize("input", dict_to_tuples(test_data, "get_tracks"))
def test_get_user_data_spotify_tracks(input):
    placeholder_test(input, usecases.get_user_tracks, OnLoadSpotify)


def placeholder_test(input, usecase: type, onload):
    ip = input[0]
    ip.reverse()
    exp_out = input[1]

    def mock_call(func, params, inp):
        return ip.pop()

    monkeypatch.setattr(SpotifyAPICall, "_call", mock_call)

    out = obj_to_dict_items(usecase(onload))

    print(json.dumps(out))
    print(json.dumps(exp_out))

    assert exp_out == out
