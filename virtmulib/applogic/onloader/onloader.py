from abc import ABC, abstractmethod
from pydantic import BaseModel

from virtmulib.entities import Playlist, User, Album, Track, Library, Artist, Genre


class OnLoaderAuthError(Exception):
    "User-defined exception class to wrap auth errors of onloaders."

class OnLoad(ABC):
    "Abstract class interface for onloaders."

    @staticmethod
    def login_onload_user_data() -> Library:
        "Fuction to implement the login onto the onloader service."

    @staticmethod
    def get_playlists() -> list[Playlist]:
        pass

    @staticmethod
    def get_albums() -> list[Album]:
        pass

    @staticmethod
    def get_tracks() -> list[Track]:
        pass

    @staticmethod
    def get_artists() -> list[Artist]:
        pass

class OnLoadGetType(ABC):
    
    @classmethod
    def retrieve(cls):
        pass

    @classmethod
    def read(cls):
        pass


    # def _add_to_extended_library(, obj: VMLThing) -> None:
    #     # TODO: Add a cache and only append if not in cache
    #     self._lib.append(obj)

    # @staticmethod
    # def create_or_load_track(data: dict) -> Track:
    #     # TODO: Add a cache and only append if not in cache
    #     return Track(**data)

    # @staticmethod
    # def create_or_load_album(data: dict) -> Album:
    #     # TODO: Add a cache and only append if not in cache
    #     return Album(**data)

    # @staticmethod
    # def create_or_load_artist(data: dict) -> Artist:
    #     # TODO: Add a cache and only append if not in cache
    #     return Artist(**data)

    # @staticmethod
    # def create_or_load_user(data: dict) -> User:
    #     # TODO: Add a cache and only append if not in cache
    #     return User(**data)

    # @staticmethod
    # def create_or_load_playlist(data: dict) -> Playlist:
    #     # TODO: Add a cache and only append if not in cache
    #     return Playlist(**data)

    # @staticmethod
    # def create_or_load_genre(data: dict) -> Genre:
    #     # TODO: Add a cache and only append if not in cache
    #     return Genre(**data)
