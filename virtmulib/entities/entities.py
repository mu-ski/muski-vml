import datetime
from abc import ABC
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict, HttpUrl

from virtmulib.entities.misc_definitions import (
        PyObjectId, MusicModel, ReleaseTypeEnum, AIAgentSetup)

class ExternalIDs(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)

    musicbrainz: Optional[UUID4] = None
    upc: Optional[str] = None
    isrc: Optional[str] = None
    discogs: Optional[str] = None
    spotify: Optional[str] = None

class VMLThing(BaseModel, ABC):
    model_config = ConfigDict(validate_assignment=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    thumb: Optional[HttpUrl] = None
    genres: Optional[list["Genre"]] = None
    date: Optional[datetime.date] = datetime.date(3000, 1, 1)
    popularity: Optional[int] = None
    model: Optional[MusicModel] = None
    ext_ids: Optional[ExternalIDs] = ExternalIDs()
    related: Optional[list["VMLThing"]] = []

class Genre(VMLThing):
    pass

class Artist(VMLThing):
    albums: Optional[list["Album"]] = None
    tracks: Optional[list["Track"]] = None

class Track(VMLThing):
    artist: Artist
    artist_sec: Optional[Artist] = None
    albums: Optional[list["Album"]] = []
    playlists: Optional[list[PyObjectId]] = []

class Album(VMLThing):
    artist: Artist
    artist_sec: Optional[Artist] = None
    tracklist: Optional[list[Track]] = []
    label: Optional[str] = None
    release_type: Optional[ReleaseTypeEnum] = None

class Playlist(VMLThing):
    creator: "User"
    ai_agent_setup: Optional[AIAgentSetup] = None
    tracklist: Optional[list[Track]] = []
    description: Optional[str] = None

class Library(VMLThing):
    # TODO: use bigtree instead
    # or find something that works with pydantic out of the box
    name: str = ""
    parent: Optional["Library"] = None
    children: Optional[list["Library"]] = []
    artists: Optional[list[Artist]] = []
    playlists: Optional[list[Playlist]] = []
    albums: Optional[list[Album]] = []
    tracks: Optional[list[Track]] = []
    genres: Optional[list[Genre]] = []

    def add(self, obj: VMLThing) -> None:
        if type(obj) == Album:
            self.albums.append(obj)
        elif type(obj) == Artist:
            self.artists.append(obj)
        elif type(obj) == Playlist:
            self.playlists.append(obj)
        elif type(obj) == Track:
            self.tracks.append(obj)

    # def init(self, artists, playlists, albums, tracks):
    #     """Given a set of lists of music items, initialize the object with thin copies of them"""
    #     pass

    def add_child(self, node: "Library"):
        children.append(node)

class User(VMLThing):
    email: Optional[EmailStr] = None
    lib: Optional[Library] = None
    # lib_extended: Optional[Library] = None
