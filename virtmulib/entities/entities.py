from abc import ABC
import re
import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, UUID4, Field

from virtmulib.entities.py_object_id import PyObjectId

class SimpleDate:
	dt: datetime.date
	def __init__(self, dt: str) -> list:
		lis = [int(i) for i in dt.split('-')]
		if len(lis) < 3:
			default_date = [1900, 1, 1]
			lis.extend(default_date[len(lis):])
		self.dt=datetime.date(*lis) 


class AIAgentEnum(Enum):
	llamma_2_70gb = 'llamma_2_70gb'

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


class AIAgentSetup(BaseModel):
	agent: AIAgentEnum
	setup: Optional[str] = None


# class IDSources(Enum):
# 	musicbrainz = 'musicbrainz'
# 	upc = 'upc'
# 	isrc = 'isrc'
# 	discogs = 'discogs'
# 	spotify = 'spotify'


class ExternalIDs(BaseModel):
	musicbrainz: Optional[UUID4] = None
	upc: Optional[str] = None
	isrc: Optional[str] = None
	discogs: Optional[str] = None
	spotify: Optional[str] = None


class MusicThing(BaseModel, ABC):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: str
	genres: Optional[list[Genre]] = None
	date: Optional[datetime.date] = None
	popularity: Optional[int] = None
	music_model: Optional[MusicModel] = None
	ext_ids: Optional[ExternalIDs] = ExternalIDs()

	class Config:
		validate_assignment = True

class Artist(MusicThing):
	#active_from: Optional[date] = None
	#active_to: Optional[date] = None
	albums: Optional[list['Album']] = None
	tracks: Optional[list['Track']] = None


class Track(MusicThing):
	artist: Artist
	artist_sec: Optional[Artist] = None
	album_ids: Optional[list[PyObjectId]] = []


class Album(MusicThing):
	artist: Artist
	artist_sec: Optional[Artist] = None
	tracklist: Optional[list[Track]] = []
	label: Optional[str] = None
	release_type: Optional[ReleaseTypeEnum] = None


class Person(BaseModel):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: Optional[str] = None
	ext_ids: Optional[ExternalIDs] = ExternalIDs()
	music_model: Optional[MusicModel] = None
	artists: Optional[list[Artist]] = []
	playlists: Optional[list['Playlist']] = []
	albums: Optional[list[Album]] = []
	tracks: Optional[list[Track]] = []
	genres: Optional[list[Genre]] = []
	
	class Config:
		validate_assignment = True

class Playlist(MusicThing):
	creator: Person
	ai_agent_setup: Optional[AIAgentSetup] = None
	tracklist: Optional[list[Track]] = []
	description: Optional[str] = None


class User(Person):
	email: Optional[EmailStr] = None

	class Config:
		validate_assignment = True

	def make_person(self) -> Person:
		return Person(self.model_dump(exclude='email'))