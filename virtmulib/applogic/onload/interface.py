"""
OnLoaders are tools to retrieve user data from external services into the app.

Currently, Spotify is the only implemented onLoader, but others are planned.

"""
from abc import ABC, abstractmethod
from attrs import define
from enum import Enum

from virtmulib.entities import (
        VMLThing, Playlist, Album, 
        Track, Library, Artist, User)


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


@define
class OnLoaderAction(ABC):
    """
    An abstract class to refactor common functionalities of onLoad actions (getAlbums,..)

    Args:
        onload (OnLoad): OnLoader class implementation (one per service)
        f_name (str): function 

    """

    OnLoad: type
    f_name: str

    def execute(self) -> VMLThing | None:
        """
        It takes a function name and binds it to the corresponding function in the onLoad class.
        """
        try:
            func = getattr(self.OnLoad, self.f_name)
            return func()
        except OnLoadAuthError as e:
            print(str(e))
            return None


@define
class GetUserData(OnLoaderAction):
    f_name: str = "login_onload_user_data"


@define
class GetUserDataPlaylists(OnLoaderAction):
    f_name: str = "get_playlists"


@define
class GetUserDataAlbums(OnLoaderAction):
    f_name: str = "get_albums"


@define
class GetUserDataTracks(OnLoaderAction):
    f_name: str = "get_tracks"


@define
class GetUserDataArtists(OnLoaderAction):
    f_name: str = "get_artists"


