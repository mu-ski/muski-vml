import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from virtmulib.entities import (
    Playlist,
    User,
    Album,
    Track,
    Library,
    Artist,
    VMLThing,
    Genre,
)

from virtmulib.entities.misc_definitions import ReleaseTypeEnum

from virtmulib.applogic.onloader import OnLoad, OnLoaderAuthError, OnLoadGetType

TEST = True
SCOPES = [
    "user-library-read",
    "user-follow-read",
    "user-top-read",
    "playlist-modify-public",
    "playlist-read-private",
]
CNT: int = 0


class OnLoadSpotify(OnLoad):
    @classmethod
    def login_signup(cls) -> Spotify:
        sp = None
        try:
            sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
        except SpotifyOauthError as error:
            raise OnLoaderAuthError("Something went wrong while signing up.") from error
        return sp

    @classmethod
    def login_onload_user_data(cls) -> None:
        sp = OnLoadSpotify.login_signup()
        if sp is not None:
            user = SpotifyGetUser.read(sp.me())

        pl = cls.get_playlists(sp)
        albs = cls.get_albums(sp)
        trs = cls.get_tracks(sp)
        arts = cls.get_artists(sp)

        user.lib = Library(playlists=pl, artists=arts, albums=albs, tracks=trs)
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
    @classmethod
    def _call(cls, func: type, params=None, inp=None):
        """Routing all the API calls here for mocking and rate limits"""
        global CNT
        # if _t is None:
        #     _t = time.time()
        CNT += 1
        if params is None or params == {}:
            if inp is None:
                return func()
            return func(inp)
        if inp is None:
            return func(**params)
        return func(inp, **params)

    @classmethod
    def execute(cls, spot_func: type, limit=20, inp=None, mx=2000) -> list[VMLThing]:
        if TEST:
            limit = 2
            mx = 2
        items = []
        for offset in range(0, mx, limit):
            res = cls._call(
                spot_func, params={"limit": limit, "offset": offset}, inp=inp
            )
            items.extend(res.get("items"))
            if res["items"] == [] or res["next"] is None:
                break
        return items


class SpotifyGetDate(OnLoadGetType):
    @classmethod
    def read(cls, data: str) -> datetime.date:
        lis = [int(i) for i in data.split("-")]
        if len(lis) < 3:
            default_date = [1900, 1, 1]
            lis.extend(default_date[len(lis) :])
        return datetime.date(*lis)


class SpotifyGetUser(OnLoadGetType):
    @classmethod
    def read(cls, data: dict) -> User:
        return User.get_or_create(
            {
                "email": data.get("email"),
                "name": data.get("display_name"),
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
            it["genres"] = grs

        imgs = data.get("images")
        it["thumb"] = (
            imgs[0].get("url") if imgs is not None and len(imgs) != 0 else None
        )

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
        if alb.date < tr.date:
            tr.date = alb.date
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
        if alb["release_type"] == ReleaseTypeEnum.COMPILATION:
            alb["artist"] = SpotifyGetArtists.read({"artists": [{"name": "Various"}]})

        alb["label"] = data.get("label")
        alb["date"] = SpotifyGetDate.read(data.get("release_date"))

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


class SpotifyGetGenres(OnLoadGetType):
    @classmethod
    def read(data: str) -> Genre:
        return Genre.get_or_create({"name": data})


# def get_related_artists(art_id: str) -> list[Artist]:
#     # artist_related_artists(artist_id)
#     pass

# def _get_extended_library(lib: Library) -> Library:
#     pass


# def _append_to_read(obj: VMLThing) -> None:
#     # Add a cache and only append if not in cache
#     _lib_to_read.add(obj)

# # Get Tracks' Audio Features
# # Get audio features for multiple tracks based on their Spotify IDs.
