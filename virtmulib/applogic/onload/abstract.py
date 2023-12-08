from abc import ABC, abstractmethod

from virtmulib.entities import VMLThing, Playlist, Album, Track, Library, Artist, User


class OnLoad(ABC):
    "Abstract class interface for onloaders."

    @classmethod
    @abstractmethod
    def login_onload_user_data(cls) -> User:
        "Fuction to implement the login onto the onloader service."
        pass

    @classmethod
    @abstractmethod
    def get_playlists(cls) -> list[Playlist]:
        pass

    @classmethod
    @abstractmethod
    def get_albums(cls) -> list[Album]:
        pass

    @classmethod
    @abstractmethod
    def get_tracks(cls) -> list[Track]:
        pass

    @classmethod
    @abstractmethod
    def get_artists(cls) -> list[Artist]:
        pass


class OnLoadGetType(ABC):
    @classmethod
    @abstractmethod
    def retrieve(cls, *args):
        pass

    @classmethod
    @abstractmethod
    def read(cls, *args):
        pass


class OnLoadAuthError(Exception):
    "Exception to wrap auth errors of onloaders"
