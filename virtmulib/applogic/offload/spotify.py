import spotipy
from time import sleep
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyOauthError

#from roeld.track import track, tracklist
from . import search_utils as utils


# https://github.com/spotipy-dev/spotipy/issues/230
# import spotipy.util as util
# token = util.prompt_for_user_token(username, client_id, client_secret, redirect_uri)

#user-library-read
#user-top-read
#user-read-email
#playlist-modify-public

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


def make_playlist(tracklist):
    sp = login_signup()
    # scope = 'playlist-modify-public'
    # username = 'z6uxnjgt70r30gea6ykxr92eq'
    # sp = spotipy.Spotify(
    #     auth_manager=SpotifyOAuth(
    #         scope=scope,
    #         #client_id=client_id,
    #         #client_secret=client_secret,
    #         #redirect_uri='http://localhost:8888/callback/',
    #         username=username
    #     )
    # )
    user_display = "nkas"
    theme = "The Residents (II)"
    pl_title = theme + " (A MuWiz list)"
    pl_desc = "Custom made for " + user_display+ ", by the MuWiz team"
    pl = sp.user_playlist_create(user=sp.me()['id'],name=pl_title, public=True, collaborative=False, description=pl_desc)
    playlist_id = pl['id']
    #playlist_id = '7gFNxShDnCQb3pcEeIlJO8'
    
    #MuWiz

    #tr_ls = tracklist.iter()
    hit_ls = []
    for tr in tracklist:
        print(tr)
        tr_hit = search_top_hit(tr, sp)
        if tr_hit != None:
            hit_ls.append(tr_hit)
        #sleep( 1 )
    sp.playlist_add_items(playlist_id, hit_ls)
    #sp.user_playlist_add_tracks(sp.me()['id'], playlist_id, hit_ls)


def search_top_hit(tr, sp):
    #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    s = sp.search(tr, type='track')
    
    
    trk_mtch = format_track_match(s['tracks']['items'][0])
    trk_id = s['tracks']['items'][0]['uri']
    
    if utils.two_in(trk_mtch, tr):
        return trk_id


    trk_mtch = format_track_match(s['tracks']['items'][1])
    trk_id = s['tracks']['items'][1]['uri']
    
    if utils.two_in(trk_mtch, tr):
        return trk_id
    
    
def match_trk(original, match):
    return utils.two_in(match.get_artist(), original.get_artist()) and utils.two_in(match.get_song_title(), original.get_song_title()) and match.get_title().lower().find('karaoke') == -1
        
def format_track_match(i):
    return i['artists'][0]['name'] + ' - ' + i['name']