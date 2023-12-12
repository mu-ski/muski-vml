import datetime
from abc import ABC
# from functools import cache
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


class ExternalIDs(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)

    musicbrainz: Optional[UUID4] = None
    upc: Optional[str] = None
    isrc: Optional[str] = None
    discogs: Optional[str] = None
    spotify: Optional[str] = None

    # def get_ids_namespaced(self) -> list[str]:
    #     ids = self.model_dump(exclude_defaults=True)
    #     ids = set(ids.items())
    #     return [f'{e[0]}:{e[1]}' for e in ids]

CACHE = {}


class VMLThing(BaseModel, ABC):
    model_config = ConfigDict(validate_assignment=True)

    genres: list["Genre"] = []
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    thumb_url: Optional[str] = None
    date: datetime.date = datetime.date(3000, 1, 1)
    popularity: Optional[int] = None
    model: Optional[MusicModel] = None
    ext_ids: ExternalIDs = ExternalIDs()
    related: Optional[list["VMLThing"]] = []


class VMLThing(BaseModel, ABC):
    model_config = ConfigDict(validate_assignment=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    genres: list["Genre"] = []
    thumb_url: Optional[str] = None
    date: datetime.date = datetime.date(3000, 1, 1)
    popularity: Optional[int] = None
    model: Optional[MusicModel] = None
    ext_ids: ExternalIDs = ExternalIDs()
    related: Optional[list["VMLThing"]] = []

    # @classmethod
    # def get_or_create_(cls, data: dict):
    #     #ids = json.dumps(data['ext_ids'])
    #     for source in data['ext_ids']:
    #         if data['ext_ids'][source] is not None:
    #             uri= f'{source}:{data["ext_ids"][source]}'
    #             if uri in CACHE.keys():
    #                 return CACHE[uri]
        
    #     # Retrieve obj if in DB
    #     obj = cls(**data)
        
    #     ext_ids = obj.ext_ids.model_dump(exclude_defaults=True)
    #     for source in ext_ids:
    #         uri= f'{source}:{data["ext_ids"][source]}'
    #         CACHE[uri] = obj

    #     return obj

    @classmethod
    def get_or_create(cls, data: dict):
        # ids = {id for id in data['ext_ids'].values() if id is not None}
        # 

        for source in data['ext_ids']:
            if data['ext_ids'][source] is not None:
                if data['ext_ids'][source] in CACHE.keys():
                    return CACHE[data['ext_ids'][source]]
        
        # Retrieve obj if in DB
        obj = cls(**data)
        
        ext_ids = obj.ext_ids.model_dump(exclude_defaults=True)
        for id in ext_ids.values():
            CACHE[id] = obj

        return obj

    @classmethod
    def get_or_create_simple(cls, data: dict):
        # ids = {id for id in data['ext_ids'].values() if id is not None}
        # 

        for source in data['ext_ids']:
            if data['ext_ids'][source] is not None:
                if data['ext_ids'][source] in CACHE.keys():
                    return CACHE[data['ext_ids'][source]]
        
        # Retrieve obj if in DB
        obj = cls(**data)
        
        ext_ids = obj.ext_ids.model_dump(exclude_defaults=True)
        for id in ext_ids.values():
            CACHE[id] = obj

        return obj

    
    # @classmethod
    # @cache
    # def _get_or_create(cls, data):
    #     # Retrieve obj if in DB
    #     return cls(**json.loads(data))


class Genre(VMLThing):
    pass


class Artist(VMLThing):
    albums: list["VMLThing"] = []
    tracks: list["VMLThing"] = []


class Track(VMLThing):
    artist: VMLThing
    artist_sec: Optional[VMLThing] = None
    albums: list["Album"] = []
    playlists: list[PyObjectId] = []


class Album(VMLThing):
    artist: VMLThing
    artist_sec: Optional[VMLThing] = None
    tracklist: list[VMLThing] = []
    label: Optional[str] = None
    release_type: Optional[ReleaseTypeEnum] = None


class Playlist(VMLThing):
    creator: "User"
    ai_agent_setup: Optional[AIAgentSetup] = None
    tracklist: list[VMLThing] = []
    description: Optional[str] = None


class Library(VMLThing):
    # Consider using a built tree datasrtuct like bigtree instead
    # Better if something that works with pydantic out of the box
    name: str = ""
    parent: Optional["Library"] = None
    children: list["Library"] = []
    artists: list[VMLThing] = []
    playlists: list[VMLThing] = []
    albums: list[VMLThing] = []
    tracks: list[VMLThing] = []
    genres: list[VMLThing] = []

    # def add(self, obj: VMLThing) -> None:
    #     if isinstance(obj, Album):
    #         self.albums.append(obj)
    #     elif isinstance(obj, Artist):
    #         self.artists.append(obj)
    #     elif isinstance(obj, Playlist):
    #         self.playlists.append(obj)
    #     elif isinstance(obj, Track):
    #         self.tracks.append(obj)

    # def init(self, artists, playlists, albums, tracks):
    #     """Given a set of lists of music items, initialize the object with thin copies of them"""
    #     pass

    def add_child(self, node: "Library"):
        self.children.append(node)


class User(VMLThing):
    email: Optional[EmailStr] = None
    lib: Optional[Library] = None
    lib_extended: Optional[Library] = None
