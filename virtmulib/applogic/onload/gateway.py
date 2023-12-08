"""
OnLoaders are tools to retrieve user data from external services into the app.

Currently, Spotify is the only implemented onLoader, but others are planned.

"""
from abc import ABC, abstractmethod
from attrs import define
from enum import Enum

from virtmulib.entities import Playlist, Album, Track, Artist, User

from virtmulib.applogic.onload.abstract import OnLoad, OnLoadAuthError


@define
class GetUserData:
    on_load: OnLoad

    def execute(self) -> list[User] | None:
        "Calls the corresponding function in the onLoad class."
        try:
            return self.on_load.login_onload_user_data()
        except OnLoadAuthError as e:
            print(str(e))
            return None


@define
class GetUserDataPlaylists:
    on_load: OnLoad

    def execute(self) -> list[Playlist] | None:
        "Calls the corresponding function in the onLoad class."
        try:
            return self.on_load.get_playlists()
        except OnLoadAuthError as e:
            print(str(e))
            return None


@define
class GetUserDataAlbums:
    on_load: OnLoad

    def execute(self) -> list[Album] | None:
        "Calls the corresponding function in the onLoad class."
        try:
            return self.on_load.get_albums()
        except OnLoadAuthError as e:
            print(str(e))
            return None


@define
class GetUserDataTracks:
    on_load: OnLoad

    def execute(self) -> list[Track] | None:
        "Calls the corresponding function in the onLoad class."
        try:
            return self.on_load.get_tracks()
        except OnLoadAuthError as e:
            print(str(e))
            return None


@define
class GetUserDataArtists:
    on_load: OnLoad

    def execute(self) -> list[Artist] | None:
        "Calls the corresponding function in the onLoad class."
        try:
            return self.on_load.get_artists()
        except OnLoadAuthError as e:
            print(str(e))
            return None
