import abc
from abc import ABC
from pydantic import BaseModel, EmailStr
from enum import Enum

from virtmulib.entities import Playlist, User, Track, Album, Artist, Library, VMLThing

# class OnLoaderEnum(Enum):
# 	spotify = 'spotify'

class OnLoaderAuthError(Exception):
	"User-defined exception class to wrap auth errors of onloaders."
	pass

class OnLoader(BaseModel, ABC):
	_lib: Library = Library()

	"Abstract class interface for onloaders."

	@abc.abstractmethod
	def login_signup(self) -> EmailStr:
		"Fuction to implement the login onto the onloader service."
		pass

	@abc.abstractmethod
	def get_playlists(self) -> list[Playlist]:
		pass

	@abc.abstractmethod
	def get_albums(self) -> list[Album]:
		pass
	
	@abc.abstractmethod
	def get_tracks(self) -> list[Track]:
		pass

	@abc.abstractmethod
	def get_artists(self) -> list[Artist]:
		pass

	def _add_to_extended_library(self, obj: VMLThing) -> None:
		# TODO: Add a cache and only append if not in cache
		self._lib.append(obj)

	def _create_or_load_track(self, data: dict) -> Track:
		return Track(**data)

	def _create_or_load_album(self, data: dict) -> Album:
		return Album(**data)

	def _create_or_load_artist(self, data: dict) -> Artist:
		return Artist(**data)

	def _create_or_load_user(self, data: dict) -> User:
		return User(**data)

	def _create_or_load_playlist(self, data: dict) -> Playlist:
		return Playlist(**data)


