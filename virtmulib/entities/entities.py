from abc import ABC
import re
from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, UUID4

class AIAgentEnum(Enum):
	llamma_2_70gb = 'llamma_2_70gb'


class ReleaseTypeEnum(Enum):
	album = 'album'
	single = 'single'
	compilation = 'compilation'
	user_made = 'user_made'

class AbsUser(BaseModel, ABC):
	pass

class Artist(BaseModel):
	id: Optional[int] = None
	name: Optional[str] = None
	active_from: Optional[date] = None
	active_to: Optional[date] = None
	musicbrainz_id: Optional[UUID4] = None
	spotify_id: Optional[str] = None


class Track(BaseModel):
	id: int = None
	name: str
	artist: Artist
	secondary_artist: Optional[Artist] = None
	date: Optional[date]
	musicbrainz_id: Optional[UUID4] = None
	isrc_id: Optional[str] = None
	spotify_id: Optional[str] = None
	

class Album(BaseModel):
	id: int = None	
	name: str	
	artist: Artist
	secondary_artist: Optional[Artist] = None
	tracklist: Optional[list[Track]] = []
	date: Optional[date]
	label: Optional[str] = None
	release_type: Optional[ReleaseTypeEnum] = None
	musicbrainz_id: Optional[UUID4] = None
	isrc_id: Optional[str] = None
	spotify_id: Optional[str] = None


class Playlist(BaseModel):
	id: int = None
	name: str
	creator: AbsUser
	tracklist: list[Track]
	description: Optional[str] = None
	date: Optional[date] = None
	id_at_source: Optional[str] = None
	source: Optional[str] = None


class AIPlaylist(Playlist):
	ai_model: AIAgentEnum
	ai_model_setup: Optional[str] = None


class Genre(BaseModel):
	name: str	
	musicbrainz_id: Optional[UUID4] = None


class UserLibrary(BaseModel):
	id: int = None	
	artists: Optional[list[Artist]] = []
	playlists: Optional[list[Playlist]] = []
	albums: Optional[list[Album]] = []
	genres: Optional[list[Genre]] = []

	def add(self, item:BaseModel) -> None:
		if isinstance(item, Artist):
			self.artists.append(item)
			#self._add_artist(item)
		elif isinstance(item, Playlist):
			self.playlists.append(item)
			#self._add_playlist(item)
		elif isinstance(item, Album):
			self.albums.append(item)
			#self._add_album(item)
		elif isinstance(item, Genre):
			self.genres.append(item)
			#self._add_genre(item)

class User(AbsUser):
	id: Optional[int] = None
	name: Optional[str] = None
	email: Optional[EmailStr] = None
	library: Optional[UserLibrary] = UserLibrary()
	id_at_source: Optional[str] = None
	source: Optional[str] = None

