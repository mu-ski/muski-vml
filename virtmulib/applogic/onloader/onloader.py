import abc
from abc import ABC
from pydantic import BaseModel, EmailStr
from enum import Enum

from virtmulib.entities import Playlist, User, Track, Album, Artist

class OnLoaderEnum(Enum):
	Spotify = 'spotify'

class OnLoaderAuthError(Exception):
	"User-defined exception class to wrap auth errors of onloaders."
	pass

class OnLoader(BaseModel, ABC):	
	"Abstract class interface for onloaders."

	@abc.abstractmethod
	def login_signup(self) -> EmailStr:
		"Fuction to implement the login onto the onloader service."
		pass

	@abc.abstractmethod
	def _get_playlists(self) -> list[Playlist]:
		pass

	@abc.abstractmethod
	def _get_albums(self) -> list[Album]:
		pass
	
	@abc.abstractmethod
	def _get_tracks(self) -> list[Track]:
		pass

	@abc.abstractmethod
	def _get_artists(self) -> list[Artist]:
		pass
