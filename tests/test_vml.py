import json
import pytest
from _pytest.monkeypatch import MonkeyPatch

import virtmulib.applogic.gateway as usecases
from virtmulib.applogic.onload.spotify import SpotifyAPICall, OnLoadSpotify
from virtmulib.applogic import ai_playlister
from virtmulib.applogic.offload.spotify import make_playlist
from tests.utils import *


test_data = json.loads(open("tests/json_test_data/test.json", "r").read())
monkeypatch = MonkeyPatch()


@pytest.mark.e2e
def test_live_get_user_data_spotify():
    # monkeypatch.undo()
    user = usecases.get_user_data(OnLoadSpotify)
    obj = json.dumps(obj_to_dict(user))
    print(user.lib.get_top_tracks())
    # print(obj)
    assert obj != {}


# @pytest.mark.e2e
# def test_full_e2e():
#     user = usecases.get_user_data(OnLoadSpotify)
#     #obj = json.dumps(obj_to_dict(user))
#     top_artists = user.lib.get_top_artists()
#     user_query = f"Some Artists played: {', '.join(top_artists)}\n"
#     user_query += """
#         Top songs: Herbie Hancock - Maiden Voyage, Laika - Praire Dog
#         What music means to me: Music is what I listen to when I need to discover new feelings and new imagination
#         Liked Music: I like many kinds of music, as long as its creative, emotional, and midtempo. I like world music, I like african american music in general.
#         Music not liked: I typically don't like rock music, but there are exceptions, typically open-minded artists that are self-conscious of the role of the west in colonalism.
#         Playlist request: It is a nice sunny sunday in december and I would like to listen to some creative and relaxed world music
#         """


#     val = None
#     import contextlib
#     import os
#     with contextlib.redirect_stdout(os.devnull):
#         val = ai_playlister.inference(user_query)

#     if val:
#         title, playlist = val
#         print(title, playlist)
#         pl = make_playlist(title, playlist)
#         assert pl is not None
#     else:
#         print('Due to user excitement and usage, the limit of the (free) AI-server we use has been completed. We are working on a more permanenet solution at the moment.')

#     # print(user.lib.get_top_albums())
#     # print(user.lib.get_top_tracks())


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
