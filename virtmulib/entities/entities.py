from abc import ABC
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict

from virtmulib.entities.misc_definitions import *


class ExternalIDs(BaseModel):
	model_config = ConfigDict(extra='allow', validate_assignment=True)

	musicbrainz: Optional[UUID4] = None
	upc: Optional[str] = None
	isrc: Optional[str] = None
	discogs: Optional[str] = None
	spotify: Optional[str] = None


class VMLThing(BaseModel, ABC):
	model_config = ConfigDict(extra='allow', validate_assignment=True)
	
	id: Optional[PyObjectId] = Field(alias="_id", default=None)
	name: str
	genres: Optional[list['Genre']] = None
	date: Optional[datetime.date] = None
	popularity: Optional[int] = None
	music_model: Optional[MusicModel] = None
	ext_ids: Optional[ExternalIDs] = ExternalIDs()


class Genre(VMLThing):
	pass


class Artist(VMLThing):
	albums: Optional[list['Album']] = None
	tracks: Optional[list['Track']] = None


class Track(VMLThing):
	artist: Artist
	artist_sec: Optional[Artist] = None
	albums: Optional[list['Album']] = None


class Album(VMLThing):
	artist: Artist
	artist_sec: Optional[Artist] = None
	tracklist: Optional[list[Track]] = []
	label: Optional[str] = None
	release_type: Optional[ReleaseTypeEnum] = None


class Playlist(VMLThing):
	creator: 'User'
	ai_agent_setup: Optional[AIAgentSetup] = None
	tracklist: Optional[list[Track]] = []
	description: Optional[str] = None


class User(VMLThing):
	email: Optional[EmailStr] = None
	org: Optional['MusicOrganization'] = None


class MusicLibrary(VMLThing):
	model_config = ConfigDict(extra='allow', validate_assignment=True)

	artists: Optional[list[Artist]] = []
	playlists: Optional[list[Playlist]] = []
	albums: Optional[list[Album]] = []
	tracks: Optional[list[Track]] = []
	genres: Optional[list[Genre]] = []	


class MusicOrganization(VMLThing):
	#TODO: use bigtree instead
	name: str
	parent: Optional['MusicOrganization'] = None
	children: Optional[list['MusicOrganization']] = []
	org: Optional['MusicLibrary'] = None

	def add_child(self, node: 'MusicOrganization'):
		children.append(node)
