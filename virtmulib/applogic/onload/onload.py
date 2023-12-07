from abc import ABC

from virtmulib.entities import Playlist, Album, Track, Library, Artist


class OnLoadAuthError(Exception):
    "User-defined exception class to wrap auth errors of onloaders."


class OnLoad(ABC):
    "Abstract class interface for onloaders."

    @classmethod
    def login_onload_user_data(cls) -> Library:
        "Fuction to implement the login onto the onloader service."

    @classmethod
    def get_playlists(cls) -> list[Playlist]:
        pass

    @classmethod
    def get_albums(cls) -> list[Album]:
        pass

    @classmethod
    def get_tracks(cls) -> list[Track]:
        pass

    @classmethod
    def get_artists(cls) -> list[Artist]:
        pass


class OnLoadGetType(ABC):
    @classmethod
    def retrieve(cls, *args):
        pass

    @classmethod
    def read(cls, *args):
        pass
