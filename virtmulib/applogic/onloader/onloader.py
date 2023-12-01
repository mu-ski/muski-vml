import abc
from abc import ABC
from pydantic import BaseModel, EmailStr
from enum import Enum

from virtmulib.entities import Playlist, User, Track, Album, Artist

# class OnLoaderEnum(Enum):
# 	spotify = 'spotify'

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
	def _add_playlists(self) -> None:
		pass

	@abc.abstractmethod
	def _add_albums(self) -> None:
		pass
	
	@abc.abstractmethod
	def _add_tracks(self) -> None:
		pass

	@abc.abstractmethod
	def _add_artists(self) -> None:
		pass
