from abc import ABC, abstractmethod
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
	label: str	
	musicbrainz_id: Optional[UUID4] = None

	def __repr__(self):
		return label

class MusicModel(BaseModel):
	pass

class AIAgentSetup(BaseModel):
	agent: AIAgentEnum
	setup: Optional[str] = None

class ExternalIDs(BaseModel):
	musicbrainz: Optional[UUID4] = None
	upc: Optional[str] = None
	isrc: Optional[str] = None
	discogs: Optional[str] = None
	spotify: Optional[str] = None


class MusicThing(BaseModel, ABC):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: str
	genres: Optional[list[Genre]] = []
	date: Optional[date] = Field(default=None)
	popularity: Optional[int] = None
	music_model: Optional[MusicModel] = None
	ext_ids: Optional[ExternalIDs] = ExternalIDs()

	class Config:
		validate_assignment = True

	# @abstractmethod
	# def simple(self):
	# # 	return type(self)(id=self.id, name=self.name)
	# 	pass

class Artist(MusicThing):
	active_from: Optional[date] = Field(default=None)
	active_to: Optional[date] = Field(default=None)
	album_ids: Optional[list[PyObjectId]] = []
	track_ids: Optional[list[PyObjectId]] = []


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


class Playlist(MusicThing):
	creator_id: PyObjectId = Field(default=None)
	tracklist: Optional[list[Track]] = []
	ai_agent_setup: Optional[AIAgentSetup] = None
	description: Optional[str] = None


class VirtualLibrary(MusicThing):
	# artists: Optional[list[str]] = []
	# albums: Optional[list[str]] = []
	# tracks: Optional[list[str]] = []
	# playlist: Optional[list[str]] = []

	def add_artist(self, artist: Artist) -> None:
		pass

	def add_playlist(self, artist: Playlist) -> None:
		pass

	def add_track(self, artist: Track) -> None:
		pass

	def add_album(self, artist: Album) -> None:
		pass


# class MusicOrganization(BaseModel):
# 	name: str
# 	parent: Optional['MusicOrganization'] = None
# 	children: Optional[list['MusicOrganization']] = []
# 	virt_lib: Optional['VirtualLibrary'] = None

# 	def add_child(self, node: 'MusicOrganization'):
# 		children.append(node)

class Person(BaseModel):
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: Optional[str] = None
	music_model: Optional[MusicModel] = None
	id_at_source: Optional[str] = None
	source: Optional[SourcesEnum] = None
	# music_org: Optional[MusicOrganization] = None
	artists: Optional[list[Artist]] = []
	playlists: Optional[list[Playlist]] = []
	albums: Optional[list[Album]] = []
	tracks: Optional[list[Track]] = []
	genres: Optional[list[Genre]] = []
	
	class Config:
		validate_assignment = True


class User(Person):
	email: EmailStr
	def  (self) -> Person:
		return Person(
			**ob.model_dump(exclude='email')
		)


class MusicRepo(BaseModel):
	artists: Optional[list[Artist]] = []
	playlists: Optional[list[Playlist]] = []
	albums: Optional[list[Album]] = []
	tracks: Optional[list[Track]] = []
	genres: Optional[list[Genre]] = []	

