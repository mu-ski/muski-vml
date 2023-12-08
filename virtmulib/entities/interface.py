import datetime
from abc import ABC
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict, HttpUrl

from virtmulib.entities.misc import (
    PyObjectId,
    MusicModel,
    ReleaseTypeEnum,
    AIAgentSetup,
)


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
    genres: list["Genre"] = []
    date: datetime.date = datetime.date(3000, 1, 1)
    popularity: Optional[int] = None
    model: Optional[MusicModel] = None
    ext_ids: ExternalIDs = ExternalIDs()
    related: Optional[list["VMLThing"]] = []

    @classmethod
    def get_or_create(cls, data: dict):
        # Retrieve obj if in DB
        return cls(**data)


class Genre(VMLThing):
    pass


class Artist(VMLThing):
    albums: list["Album"] = []
    tracks: list["Track"] = []


class Track(VMLThing):
    artist: Artist
    artist_sec: Optional[Artist] = None
    albums: list["Album"] = []
    playlists: list[PyObjectId] = []


class Album(VMLThing):
    artist: Artist
    artist_sec: Optional[Artist] = None
    tracklist: list[Track] = []
    label: Optional[str] = None
    release_type: Optional[ReleaseTypeEnum] = None


class Playlist(VMLThing):
    creator: "User"
    ai_agent_setup: Optional[AIAgentSetup] = None
    tracklist: list[Track] = []
    description: Optional[str] = None


class Library(VMLThing):
    # Consider using a built tree datasrtuct like bigtree instead
    # Better if something that works with pydantic out of the box
    name: str = ""
    parent: Optional["Library"] = None
    children: list["Library"] = []
    artists: list[Artist] = []
    playlists: list[Playlist] = []
    albums: list[Album] = []
    tracks: list[Track] = []
    genres: list[Genre] = []

    def add(self, obj: VMLThing) -> None:
        if isinstance(obj, Album):
            self.albums.append(obj)
        elif isinstance(obj, Artist):
            self.artists.append(obj)
        elif isinstance(obj, Playlist):
            self.playlists.append(obj)
        elif isinstance(obj, Track):
            self.tracks.append(obj)

    # def init(self, artists, playlists, albums, tracks):
    #     """Given a set of lists of music items, initialize the object with thin copies of them"""
    #     pass

    def add_child(self, node: "Library"):
        self.children.append(node)


class User(VMLThing):
    email: Optional[EmailStr] = None
    lib: Optional[Library] = None
    # lib_extended: Optional[Library] = None
