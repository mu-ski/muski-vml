from abc import ABC
import re
from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, UUID4, Field

from virtmulib.entities.py_object_id import PyObjectId

class SimpleDate:
	dt: date
	def __init__(self, dt: str) -> list:
		lis = [int(i) for i in dt.split('-')]
		if len(lis) < 3:
			default_date = [1900, 1, 1]
			lis.extend(default_date[len(lis):])
		self.dt=date(*lis) 


# class AIAgentEnum(Enum):
# 	llamma_2_70gb = 'llamma_2_70gb'

class ReleaseTypeEnum(Enum):
	album = 'album'
	single = 'single'
	compilation = 'compilation'

	@classmethod
	def get_release_enum_by_name(cls, name:str) -> 'ReleaseTypeEnum':
		nm = name.lower().strip()
		if nm.find('album') > -1:
			return ReleaseTypeEnum.album
		elif nm.find('single') > -1:
			return ReleaseTypeEnum.single
		elif nm.find('compilation') > -1:
			return ReleaseTypeEnum.compilation
		return None

class SourcesEnum(Enum):
	spotify = 'spotify'

class Genre(BaseModel):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: str	
	musicbrainz_id: Optional[UUID4] = None

class MusicModel(BaseModel):
	pass

class OfficialMusicItem(BaseModel, ABC):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: str
	genres: Optional[list[Genre]] = None
	popularity: Optional[int] = None
	music_model: Optional[MusicModel] = None
	id_musicbrainz: Optional[UUID4] = None
	#id_spotify: Optional[str] = None
	id_upc: Optional[str] = None
	id_isrc: Optional[str] = None
	id_discogs: Optional[str] = None
	id_at_source: Optional[str] = None
	source: Optional[SourcesEnum] = None

	class Config:
		validate_assignment = True

class Artist(OfficialMusicItem):
	active_from: Optional[date] = None
	active_to: Optional[date] = None
	albums: Optional[list['Album']] = None
	tracks: Optional[list['Track']] = None


class Track(OfficialMusicItem):
	artist: Artist
	artist_sec: Optional[Artist] = None
	date: Optional[date]


class Album(OfficialMusicItem):
	artist: Artist
	artist_sec: Optional[Artist] = None
	tracklist: Optional[list[Track]] = []
	date: Optional[date]
	label: Optional[str] = None
	release_type: Optional[ReleaseTypeEnum] = None

class Person(BaseModel):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: Optional[str] = None
	id_at_source: str
	source: SourcesEnum
	
	class Config:
		validate_assignment = True

class Playlist(OfficialMusicItem):
	creator: Person
	ai_agent_setup: Optional[str] = None
	tracklist: Optional[list[Track]] = []
	description: Optional[str] = None


class User(BaseModel):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: Optional[str] = None
	email: Optional[EmailStr] = None
	id_at_source: Optional[str] = None
	source: Optional[SourcesEnum] = None
	music_model: Optional[MusicModel] = None
	artists: Optional[list[Artist]] = []
	playlists: Optional[list[Playlist]] = []
	albums: Optional[list[Album]] = []
	tracks: Optional[list[Track]] = []
	genres: Optional[list[Genre]] = []

	class Config:
		validate_assignment = True

	def make_person(self) -> Person:
		return Person(
			_user_id_on_system=self.id,
			name=self.name,
			id_at_source=self.id_at_source,
			source=self.source
			)
