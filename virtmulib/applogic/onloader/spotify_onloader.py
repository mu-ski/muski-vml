from pydantic import ConfigDict
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from virtmulib.entities import Playlist, User, Album, Track, Library, Artist, VMLThing

from virtmulib.entities.misc_definitions import ReleaseTypeEnum, SimpleDate

from virtmulib.applogic.onloader import OnLoader, OnLoaderAuthError

TEST = True
SCOPES = [
    "user-library-read",
    "user-follow-read",
    "user-top-read",
    "playlist-modify-public",
    "playlist-read-private",
]
CNT: int = 0


class SpotifyOnLoader(OnLoader):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # _sp: Spotify = None
    # _user: User = None
    # _t: time = None

    @staticmethod
    def _call(func: type, params=None, inp=None):
        """Routing all the API calls here for mocking and rate limits"""
        global CNT
        # if _t is None:
        #     _t = time.time()
        CNT += 1
        if params is None or params == {}:
            if inp is None:
                return func()
            else:
                return func(inp)
        else:
            if inp is None:
                return func(**params)
            else:
                return func(inp, **params)

    @staticmethod
    def call(func: type, params=None, inp=None):
        res = SpotifyOnLoader._call(func, params=params, inp=inp)
        return res

    @staticmethod
    def _get(
        spot_func: type, format_func: type, limit=20, inp=None, max=2000
    ) -> list[VMLThing]:
        if TEST:
            limit = 2
            max = 2
        items = []
        for offset in range(0, max, limit):
            res = SpotifyOnLoader.call(
                spot_func, params={"limit": limit, "offset": offset}, inp=inp
            )
            items.extend([format_func(item) for item in res.get("items")])
            if res["items"] == [] or res["next"] is None:
                break
        return items

    # def model_post_init(__context):
    #     login_signup()

    @staticmethod
    def login_signup() -> Spotify:
        sp = None
        try:
            sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
        except SpotifyOauthError as error:
            raise OnLoaderAuthError(str(error))
        return sp

    def login_onload_user_data() -> None:
        sp = SpotifyOnLoader.login_signup()
        if sp is not None:
            user = SpotifyOnLoader._format_as_user(sp.me())

        pl = SpotifyOnLoader.get_playlists(sp)

        albs = SpotifyOnLoader.get_albums(sp)

        trs = SpotifyOnLoader.get_tracks(sp)

        arts = SpotifyOnLoader.get_artists(sp)

        user.lib = Library(playlists=pl, artists=arts, albums=albs, tracks=trs)
        return user

    def get_tracks(sp: Spotify = None) -> list[Track]:
        sp = SpotifyOnLoader.login_signup() if sp is None else sp
        tracks = SpotifyOnLoader._get(
            sp.current_user_top_tracks, SpotifyOnLoader._format_as_track
        )
        tracks.extend(
            SpotifyOnLoader._get(
                sp.current_user_saved_tracks, SpotifyOnLoader._format_as_track
            )
        )
        return tracks

    def get_albums(sp: Spotify = None) -> list[Album]:
        sp = SpotifyOnLoader.login_signup() if sp is None else sp
        return SpotifyOnLoader._get(
            sp.current_user_saved_albums, SpotifyOnLoader._format_as_album
        )

    def get_playlists(sp: Spotify = None) -> list[Playlist]:
        sp = SpotifyOnLoader.login_signup() if sp is None else sp
        pls = SpotifyOnLoader._get(
            sp.current_user_playlists, SpotifyOnLoader._format_as_playlist
        )
        for pl in pls:
            if pl.tracklist == []:
                pl.tracklist = SpotifyOnLoader._get(
                    sp.playlist_items,
                    SpotifyOnLoader._format_as_track,
                    inp=pl.ext_ids.spotify,
                    limit=100,
                )
        return pls

    def get_artists(sp: Spotify = None) -> list[Artist]:
        sp = SpotifyOnLoader.login_signup() if sp is None else sp
        return SpotifyOnLoader._get(
            sp.current_user_top_artists, SpotifyOnLoader._format_as_artist
        )

    @staticmethod
    def get_related_artists(art_id: str) -> list[Artist]:
        # artist_related_artists(artist_id)
        pass

    @staticmethod
    def _get_extended_library(lib: Library) -> Library:
        pass

    @staticmethod
    def _get_a_list_of_tracks(tracks: list, sp: Spotify = None) -> list[Track]:
        sp = SpotifyOnLoader.login_signup() if sp is None else sp
        if "items" in tracks.keys():
            tracks = tracks["items"]
        tr_ids = [tr.get("id") for tr in tracks.get("items")]
        trs_data = SpotifyOnLoader.call(sp.tracks, inp=tr_ids).get("tracks")
        return [SpotifyOnLoader.create_or_load_track(tr_data) for tr_data in trs_data]

    @staticmethod
    def _format_common_fields(item: dict) -> dict:
        it = {}
        it["name"] = item.get("name")
        it["ext_ids"] = {"spotify": item.get("id")}

        if "genres" in item.keys():
            grs = [SpotifyOnLoader.create_or_load_genre(name=g) for g in item["genres"]]
            it["genres"] = grs

        imgs = item.get("images")
        it["thumb"] = (
            imgs[0].get("url") if imgs is not None and len(imgs) != 0 else None
        )

        if "artists" in item.keys():
            arts = item.get("artists")
            it["artist"] = SpotifyOnLoader._format_common_fields(arts[0])
            it["artist_sec"] = (
                SpotifyOnLoader._format_common_fields(arts[1])
                if len(arts) > 1
                else None
            )
        return it

    @staticmethod
    def _format_as_album(item: dict) -> Album:
        if "album" in item.keys():
            item = item.get("album")
        alb = SpotifyOnLoader._format_common_fields(item)
        alb["release_type"] = ReleaseTypeEnum.get_release_enum_by_name(
            item.get("album_type")
        )
        alb["label"] = item.get("label")
        alb["date"] = SimpleDate(item.get("release_date")).dt

        alb_obj = SpotifyOnLoader.create_or_load_album(alb)
        if alb_obj.tracklist == [] and "tracks" in item.keys():
            items = item.get("tracks").get("items")
            trklst = [SpotifyOnLoader._format_as_track(itm, alb_obj) for itm in items]
            alb_obj.tracklist = trklst
        return alb_obj

    def _format_as_playlist(item: dict) -> Playlist:
        pl = SpotifyOnLoader._format_common_fields(item)
        pl["description"] = item.get("description")
        pl["creator"] = SpotifyOnLoader._format_as_user(item.get("owner"))
        pl_o = SpotifyOnLoader.create_or_load_playlist(pl)
        return pl_o

    @staticmethod
    def _format_as_track(res: dict, alb=None) -> Track:
        if "track" in res.keys():
            res = res.get("track")
        t = SpotifyOnLoader._format_common_fields(res)
        if "external_ids" in res.keys():
            t["ext_ids"]["upc"] = res.get("external_ids").get("upc")
            t["ext_ids"]["isrc"] = res.get("external_ids").get("isrc")
        tr = SpotifyOnLoader.create_or_load_track(t)
        if alb is None and "album" in res.keys():
            al = res.get("album")
            al["artist"] = t["artist"]
            alb = SpotifyOnLoader._format_as_album(al)
            tr.albums.append(alb)
        if alb.date < tr.date:
            tr.date = alb.date
        return tr

    @staticmethod
    def _format_as_artist(item: dict) -> Artist:
        return SpotifyOnLoader.create_or_load_artist(
            SpotifyOnLoader._format_common_fields(item)
        )

    @staticmethod
    def _format_as_user(item: dict) -> User:
        return SpotifyOnLoader.create_or_load_user(
            {
                "email": item.get("email"),
                "name": item.get("display_name"),
                "ext_ids": {"spotify": item.get("id")},
            }
        )

    # def _append_to_read(obj: VMLThing) -> None:
    #     # TODO: Add a cache and only append if not in cache
    #     _lib_to_read.add(obj)


# Get Tracks' Audio Features
# Get audio features for multiple tracks based on their Spotify IDs.
