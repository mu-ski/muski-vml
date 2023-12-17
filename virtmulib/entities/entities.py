import datetime
from abc import ABC
import json
from typing import Optional
import json
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict#, HttpUrl

from virtmulib.entities.utils import (
    PyObjectId,
    ReleaseTypeEnum,
    AIAgentSetup
)


class MusicModel(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)
    genres: list[str] = []
    popularity: Optional[int] = None
    related: Optional[list["BaseModel"]] = []
    date: datetime.date = datetime.date(3000, 1, 1)
    

class ExternalIDs(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)
    musicbrainz: Optional[UUID4] = None
    upc: Optional[str] = None
    isrc: Optional[str] = None
    discogs: Optional[str] = None
    spotify: Optional[str] = None

#class VMLThing(BaseModel):

class SimpleArtist(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class Artist(SimpleArtist):
    music_model: Optional[MusicModel] = None
    albums: list["SimpleAlbum"] = []
    tracks: list["SimpleTrack"] = []
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class SimpleTrack(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    artist: SimpleArtist
    artist_sec: Optional[SimpleArtist] = None

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class Track(SimpleTrack):
    albums: list["SimpleAlbum"] = []
    music_model: Optional[MusicModel] = None
    occurs_in: list[PyObjectId] = []
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class SimpleAlbum(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class Album(SimpleAlbum):
    artist: SimpleArtist
    artist_sec: Optional[SimpleArtist] = None
    tracklist: list[SimpleTrack] = []
    music_model: Optional[MusicModel] = None
    label: Optional[str] = None
    release_type: Optional[ReleaseTypeEnum] = None
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class SimplePlaylist(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    creator: "SimpleUser"
    description: Optional[str] = None

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class Playlist(SimplePlaylist):
    music_model: Optional[MusicModel] = None
    tracklist: list[SimpleTrack] = []
    ai_agent_setup: Optional[AIAgentSetup] = None
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class Library(BaseModel):
    # Consider using a built tree datasrtuct like bigtree instead
    # Better if something that works with pydantic out of the box
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    music_model: Optional[MusicModel] = None
    artists: list[SimpleArtist] = []
    playlists: list[SimplePlaylist] = []
    albums: list[SimpleAlbum] = []
    tracks: list[SimpleTrack] = []

    parent: Optional["Library"] = None
    children: list["Library"] = []

    def add_child(self, node: "Library"):
        self.children.append(node)

    # def get_top_tracks(self):
    #     return self.get_top(self.tracks)

    # def get_top(self, lis: list[BaseModel]) -> str:
    #     cache = {}
    #     for i in lis:



class SimpleUser(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    music_model: Optional[MusicModel] = None

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class User(SimpleUser):
    email: Optional[EmailStr] = None
    lib: Optional[Library] = None
    lib_extended: Optional[Library] = None
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()