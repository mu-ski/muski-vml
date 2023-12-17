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

class VMLThing(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)

class SimpleArtist(VMLThing):
    pass

class Artist(SimpleArtist):
    music_model: Optional[MusicModel] = None
    albums: list["SimpleCollection"] = []
    tracks: list["SimpleTrack"] = []
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class SimpleTrack(VMLThing):
    artist: SimpleArtist
    artist_sec: Optional[SimpleArtist] = None


class Track(SimpleTrack):
    albums: list["SimpleCollection"] = []
    music_model: Optional[MusicModel] = None
    occurs_in: list[PyObjectId] = []
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class SimpleCollection(VMLThing):
    tracklist: list[SimpleTrack] = []

    def get_top_artists(self):
        cache = {}
        for item in self.tracklist:
            if item.artist.name not in cache.keys():
                cache[item.artist.name] = 1
            else: 
                cache[item.artist.name] += 1
        # items = list(cache.items())
        # items.sort(key=lambda a:a[1])
        # items = items[-20:] if len(items) > 20 else items
        return cache
        #return dict(items)


class Album(SimpleCollection):
    artist: SimpleArtist
    artist_sec: Optional[SimpleArtist] = None
    tracklist: list[SimpleTrack] = []
    music_model: Optional[MusicModel] = None
    label: Optional[str] = None
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()
    release_type: Optional[ReleaseTypeEnum] = None


class Playlist(SimpleCollection):
    creator: "SimpleUser"
    description: Optional[str] = None
    music_model: Optional[MusicModel] = None
    ai_agent_setup: Optional[AIAgentSetup] = None
    thumb_url: Optional[str] = None
    ext_ids: ExternalIDs = ExternalIDs()


class Library(BaseModel):
    # Consider using a built tree datasrtuct like bigtree instead
    # Better if something that works with pydantic out of the box
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    music_model: Optional[MusicModel] = None
    artists: list[SimpleArtist] = []
    playlists: list[SimpleCollection] = []
    albums: list[SimpleCollection] = []
    tracks: list[SimpleTrack] = []

    parent: Optional["Library"] = None
    children: list["Library"] = []

    def add_child(self, node: "Library"):
        self.children.append(node)

    def get_top_artists(self):
        arts = {}
        
        # go through the playlists and fetch artists frequency
        for pl in self.playlists:
            arts1 = pl.get_top_artists()
            for key in arts1.keys():
                if key in arts.keys():
                    arts[key] += 1
                else:
                    arts[key] = 1
        
        # go through the albums and fetch artists frequency
        for alb in self.albums:
            arts1 = alb.get_top_artists()
            for key in arts1.keys():
                if key in arts.keys():
                    arts[key] += 1
                else:
                    arts[key] = 1
        
        # go through all tracks
        for tr in self.tracks:
            if tr.artist.name in arts.keys():
                arts[tr.artist.name] += 1
            else:
                arts[tr.artist.name] = 1
        
        # go through the list of artists
        artists = [art.name for art in self.artists]

        if len(artists) >= 20:
            return artists
        else:
            items = list(arts.items())
            items.sort(key=lambda a:a[1])
            items = items[-20+len(artists) : ] \
                        if len(items) > 20-len(artists) \
                        else items
            artists.extend([item[0] for item in items])
            return artists


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