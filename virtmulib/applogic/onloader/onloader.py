from abc import ABC, abstractmethod
from pydantic import BaseModel, EmailStr
from enum import Enum

from virtmulib.entities import Playlist, User, Track, Album, Artist, Library, VMLThing

class OnLoaderAuthError(Exception):
	"User-defined exception class to wrap auth errors of onloaders."
	pass

class OnLoader(BaseModel, ABC):
	"Abstract class interface for onloaders."

	@staticmethod
	@abstractmethod
	def login_onload_user_data() -> User:
		"Fuction to implement the login onto the onloader service."
		pass

	@staticmethod
	@abstractmethod
	def get_playlists() -> list[Playlist]:
		pass

	@staticmethod
	@abstractmethod
	def get_albums() -> list[Album]:
		pass

	@staticmethod	
	@abstractmethod
	def get_tracks() -> list[Track]:
		pass

	@staticmethod
	@abstractmethod
	def get_artists() -> list[Artist]:
		pass

	# def _add_to_extended_library(, obj: VMLThing) -> None:
	# 	# TODO: Add a cache and only append if not in cache
	# 	self._lib.append(obj)

	def create_or_load_track(data: dict) -> Track:
		# TODO: Add a cache and only append if not in cache
		return Track(**data)

	def create_or_load_album(data: dict) -> Album:
		# TODO: Add a cache and only append if not in cache
		return Album(**data)

	def create_or_load_artist(data: dict) -> Artist:
		# TODO: Add a cache and only append if not in cache
		return Artist(**data)

	def create_or_load_user(data: dict) -> User:
		# TODO: Add a cache and only append if not in cache
		return User(**data)

	def create_or_load_playlist(data: dict) -> Playlist:
		# TODO: Add a cache and only append if not in cache
		return Playlist(**data)

	def create_or_load_genre(data: dict) -> Genre:
		# TODO: Add a cache and only append if not in cache
		return Genre(**data)


