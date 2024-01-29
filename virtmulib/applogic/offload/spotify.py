import spotipy
from time import sleep
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyOauthError

# from roeld.track import track, tracklist
from . import search_utils as utils


# https://github.com/spotipy-dev/spotipy/issues/230
# import spotipy.util as util
# token = util.prompt_for_user_token(username, client_id, client_secret, redirect_uri)

# user-library-read
# user-top-read
# user-read-email
# playlist-modify-public

SCOPES = [
    "user-library-read",
    "user-follow-read",
    "user-top-read",
    "playlist-modify-public",
    "playlist-read-private",
]

# "playlist-modify-private"


def login_signup():
    sp = None
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
    except SpotifyOauthError as error:
        raise OnLoadAuthError("Something went wrong while signing up.") from error
    return sp


def make_playlist(title, tracklist):
    sp = login_signup()
    user = sp.me()
    user_display = user["display_name"]
    pl_title = title + " (A Muze list)"
    pl_desc = "Custom made for " + user_display + " by the Muze discovery platform"

    hit_ls = []
    for tr in tracklist:
        tr_hit = search_top_hit(tr, sp)
        if tr_hit != None:
            hit_ls.append(tr_hit)

    pl = sp.user_playlist_create(
        user=user["id"],
        name=pl_title,
        public=True,
        collaborative=False,
        description=pl_desc,
    )
    playlist_id = pl["id"]
    sp.playlist_add_items(playlist_id, hit_ls)
    playlist_url = pl["external_urls"]["spotify"]
    return playlist_url


def search_top_hit(tr, sp):
    results = sp.search(tr, type="track")
    track = tuple(tr.split(" - "))

    for i in range(0, 1):
        trk_id, match = get_hit_num(i, results)
        if match_trk(track, match):
            # print('>>{}', (track, match))
            return trk_id


def get_hit_num(hit, results):
    return results["tracks"]["items"][0]["uri"], format_track_match(
        results["tracks"]["items"][0]
    )


def match_trk(original, match):
    # print(original, match)
    return (
        utils.two_in(match[0], original[0], limit=1)
        and utils.two_in(match[1], original[1], limit=1)
        and match[1].lower().find("karaoke") == -1
    )


def format_track_match(i):
    return i["artists"][0]["name"], i["name"]
