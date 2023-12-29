import datetime
from functools import cache
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from virtmulib.entities import (
    Playlist,
    User,
    Album,
    Track,
    Library,
    Artist
    #VMLThing
)

from virtmulib.entities import ReleaseTypeEnum
from virtmulib.applogic.onload.abstract import OnLoad, OnLoadAuthError, OnLoadGetType

SCOPES = [
    "user-read-email",
    "user-library-read",
    "user-follow-read",
    "user-top-read",
    "playlist-modify-public",
    "playlist-read-private",
]
CNT: int = 0


class OnLoadSpotify(OnLoad):
    
    @classmethod
    def login_signup_user(cls) -> User:
        sp = OnLoadSpotify.login_signup()
        if sp:
            return SpotifyGetUser.read(sp.me())

    @classmethod
    def login_signup(cls) -> Spotify:
        sp = None
        try:
            sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
        except SpotifyOauthError as error:
            raise OnLoadAuthError("Something went wrong while signing up.") from error
        return sp

    @classmethod
    def login_onload_user_data(cls) -> User:
        sp = OnLoadSpotify.login_signup()
        if sp is not None:
            user = SpotifyGetUser.read(sp.me())

        pl = cls.get_playlists(sp)
        albs = cls.get_albums(sp)
        trs = cls.get_tracks(sp)
        arts = cls.get_artists(sp)

        user.lib = Library(playlists=pl, artists=arts, albums=albs, tracks=trs)
        
        # user.lib_extended = SpotifyGetExtendedLibrary.retrieve(user.lib)

        return user

    @classmethod
    def get_tracks(cls, sp: Spotify = None):
        return SpotifyGetTracks.retrieve(sp)

    @classmethod
    def get_albums(cls, sp: Spotify = None):
        return SpotifyGetAlbums.retrieve(sp)

    @classmethod
    def get_playlists(cls, sp: Spotify = None):
        return SpotifyGetPlaylists.retrieve(sp)

    @classmethod
    def get_artists(cls, sp: Spotify = None):
        return SpotifyGetArtists.retrieve(sp)


class SpotifyAPICall:
    """A class to route all the API calls here for mocking and rate limit control purposes"""

    @classmethod
    def execute(cls, spot_func: type, limit=20, inp=None, mx=2000) -> list[dict]:
        items = []
        key_names = {'items', 'albums', 'artists', 'tracks'}
        for offset in range(0, mx, limit):
            res = cls._call(
                spot_func, params={"limit": limit, "offset": offset}, inp=inp
            )
            key = key_names.intersection(set(res.keys())).pop()

            items.extend(res.get(key))
            if not res[key] \
                    or "next" not in res.keys() \
                    or res["next"] is None:
                break

        return items

    @classmethod
    def _call(cls, func: type, params=None, inp=None) -> dict:
        global CNT
        CNT += 1

        if params is None or params == {}:
            if inp is None:
                return func()
            return func(inp)

        if inp is None:
            return func(**params)

        # some api calls take params, others don't (and return a TypeError)
        try:
            return func(inp, **params)
        except TypeError:
            return func(inp)


class SpotifyGetYear(OnLoadGetType):
    @classmethod
    def read(cls, data: str) -> str:
        return data.split("-")[0]

class SpotifyGetUser(OnLoadGetType):
    @classmethod
    def read(cls, data: dict) -> User:
        return User.get_or_create(
            {
                "email": data.get("email"),
                "display_name": data.get("display_name"),
                "ext_ids": {"spotify": data.get("id")},
            }
        )


class SpotifyGetCommonDict(OnLoadGetType):
    @classmethod
    def read(cls, data: dict) -> dict:
        it = {}
        it["name"] = data.get("name")
        it["ext_ids"] = {"spotify": data.get("id")}

        if "genres" in data.keys():
            grs = [SpotifyGetGenres.read(g) for g in data["genres"]]
            #it["genres"] = grs
            it["music_model"] = {'genres': grs}

        if "images" in data.keys():
            imgs = data.get("images")
            it["thumb_url"] = imgs[0].get("url") if len(imgs) != 0 else None

        if "artists" in data.keys():
            arts = data.get("artists")
            it["artist"] = SpotifyGetCommonDict.read(arts[0])
            it["artist_sec"] = (
                SpotifyGetCommonDict.read(arts[1]) if len(arts) > 1 else None
            )
        return it


class SpotifyGetTracks(OnLoadGetType):
    @classmethod
    def retrieve(cls, sp: Spotify = None) -> list[Track]:
        sp = OnLoadSpotify.login_signup() if sp is None else sp

        ini_tracks = SpotifyAPICall.execute(sp.current_user_top_tracks)
        tracks = [cls.read(track) for track in ini_tracks]

        ini_tracks2 = SpotifyAPICall.execute(sp.current_user_saved_tracks)
        tracks.extend([cls.read(track) for track in ini_tracks2])

        return tracks

    @classmethod
    def read(cls, data: dict, alb=None) -> Track:
        if "track" in data.keys():
            data = data.get("track")

        t = SpotifyGetCommonDict.read(data)

        if "external_ids" in data.keys():
            t["ext_ids"]["upc"] = data.get("external_ids").get("upc")
            t["ext_ids"]["isrc"] = data.get("external_ids").get("isrc")

        tr = Track.get_or_create(t)

        if alb is None and "album" in data.keys():
            al = data.get("album")
            al["artist"] = t["artist"]
            alb = SpotifyGetAlbums.read(al)
            tr.albums.append(alb)

        # if alb.date < tr.date:
        #     tr.date = alb.date

        return tr


class SpotifyGetAlbums(OnLoadGetType):
    @classmethod
    def retrieve(cls, sp: Spotify = None) -> list[Album]:
        sp = OnLoadSpotify.login_signup() if sp is None else sp

        ini_albums = SpotifyAPICall.execute(sp.current_user_saved_albums)
        return [cls.read(album) for album in ini_albums]

    @classmethod
    def read(cls, data: dict) -> Album:
        if "album" in data.keys():
            data = data.get("album")

        alb = SpotifyGetCommonDict.read(data)

        alb["release_type"] = ReleaseTypeEnum.get_enum(data.get("album_type"))
        alb["label"] = data.get("label")
        alb["music_model"] = {"year": SpotifyGetYear.read(data.get("release_date"))}

        alb_obj = Album.get_or_create(alb)

        if alb_obj.tracklist == [] and "tracks" in data.keys():
            items = data.get("tracks").get("items")
            trklst = [SpotifyGetTracks.read(itm, alb_obj) for itm in items]
            alb_obj.tracklist = trklst

        return alb_obj


class SpotifyGetPlaylists(OnLoadGetType):
    @classmethod
    def retrieve(cls, sp: Spotify = None) -> list[Playlist]:
        sp = OnLoadSpotify.login_signup() if sp is None else sp
        ini_pls = SpotifyAPICall.execute(sp.current_user_playlists)
        pls = [cls.read(pl) for pl in ini_pls]

        for pl in pls:
            if pl.tracklist == []:
                pl_trls = SpotifyAPICall.execute(
                    sp.playlist_items,
                    inp=pl.ext_ids.spotify,
                    limit=100,
                )
                pl.tracklist = [SpotifyGetTracks.read(pl_tr) for pl_tr in pl_trls]
        return pls

    @classmethod
    def read(cls, data: dict) -> Playlist:
        pl = SpotifyGetCommonDict.read(data)

        pl["description"] = data.get("description")
        pl["creator"] = SpotifyGetUser.read(data.get("owner"))

        return Playlist.get_or_create(pl)


class SpotifyGetArtists(OnLoadGetType):
    @classmethod
    def retrieve(cls, sp: Spotify = None) -> list[Artist]:
        sp = OnLoadSpotify.login_signup() if sp is None else sp

        arts = SpotifyAPICall.execute(sp.current_user_top_artists)

        return [cls.read(art) for art in arts]

    @classmethod
    def read(cls, item: dict) -> Artist:
        return Artist.get_or_create(SpotifyGetCommonDict.read(item))


class SpotifyGetExtendedLibrary(OnLoadGetType):
    @classmethod
    def retrieve(cls, lib: Library, sp: Spotify = None) -> list[Album]:
        #import json
        #print(json.dumps(lib.model_dump(exclude_defaults=True), default=str))
        to_get = set()
        for pl in lib.playlists:
            for tr in pl.tracklist:
                for alb in tr.albums:
                    to_get.add(alb.ext_ids.spotify)
    
        to_get.union(cls._get_albums_with_no_tracklist(lib.albums))

        for artist in lib.artists:
            to_get.union(cls._get_albums_with_no_tracklist(artist.albums))

        for tr in lib.tracks:
            to_get.union(cls._get_albums_with_no_tracklist(tr.albums))

        sp = OnLoadSpotify.login_signup() if sp is None else sp

        to_get_lis = list(to_get)
        alb_objs = []

        for offset in range(0, len(to_get_lis), 20):
            albs = SpotifyAPICall.execute(sp.albums, inp=to_get_lis[offset: offset+20])
            alb_objs.extend([SpotifyGetAlbums.read(alb) for alb in albs])
        
        lib_obj = Library(albums=alb_objs)
        return lib_obj
    
    @classmethod
    def _get_albums_with_no_tracklist(cls, albs: list[Album]) -> set[str]:
        #print()
        return set([
                    alb.ext_ids.spotify 
                    for alb in albs 
                    if not alb.tracklist])



# def get_related_artists(art_id: str) -> list[Artist]:
#     # artist_related_artists(artist_id)
#     pass

# # Get Tracks' Audio Features
# # Get audio features for multiple tracks based on their Spotify IDs.
