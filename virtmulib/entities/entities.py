import datetime
from abc import ABC
import json
from typing import Optional
import json
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict, field_validator#, HttpUrl

from virtmulib.entities.utils import (
    PyObjectId,
    ReleaseTypeEnum,
    AIAgentSetup
)


class MusicModel(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)
    genres: list[str] = []
    popularity: Optional[int] = None
    text_background: Optional[str] = None
    top_artists: Optional[list[str]] = None
    top_tracks: Optional[list[str]] = None
    related: Optional[list["VMLThing"]] = []
    year: str = None

    @field_validator('year')
    @classmethod
    def validate_year(cls, v: str) -> str:
        datetime.datetime.strptime(v, "%Y")
        return v    

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
    ext_ids: ExternalIDs = ExternalIDs()

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class SimpleArtist(VMLThing):
    pass


class Artist(SimpleArtist):
    music_model: Optional[MusicModel] = None
    albums: list["SimpleAlbum"] = []
    tracks: list["SimpleTrack"] = []
    thumb_url: Optional[str] = None


class SimpleTrack(VMLThing):
    artist: SimpleArtist


class Track(SimpleTrack):
    artist_sec: Optional[SimpleArtist] = None
    albums: list["SimpleAlbum"] = []
    music_model: Optional[MusicModel] = None
    occurs_in: list[PyObjectId] = []
    thumb_url: Optional[str] = None


class SimpleAlbum(VMLThing):
    pass


class Album(SimpleAlbum):
    artist: SimpleArtist
    artist_sec: Optional[SimpleArtist] = None
    tracklist: list[SimpleTrack] = []
    music_model: Optional[MusicModel] = None
    label: Optional[str] = None
    thumb_url: Optional[str] = None
    release_type: Optional[ReleaseTypeEnum] = None

    def get_top_artists(self):
        cache = {}
        for item in self.tracklist:
            if item.artist.name not in cache.keys():
                cache[item.artist.name] = 1
            else: 
                cache[item.artist.name] += 1
        return cache


class SimplePlaylist(VMLThing):
    creator: "SimpleUser"
    description: Optional[str] = None


class Playlist(SimplePlaylist):
    music_model: Optional[MusicModel] = None
    ai_agent_setup: Optional[AIAgentSetup] = None
    thumb_url: Optional[str] = None
    tracklist: list[SimpleTrack] = []

    def get_top_artists(self):
        cache = {}
        for item in self.tracklist:
            if item.artist.name not in cache.keys():
                cache[item.artist.name] = 1
            else: 
                cache[item.artist.name] += 1
        return cache


class Library(BaseModel):
    # Consider using a built tree datasrtuct like bigtree instead
    # Better if something that works with pydantic out of the box
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    music_model: Optional[MusicModel] = None
    artists: list[SimpleArtist] = []
    playlists: list[Playlist] = []
    albums: list[Album] = []
    tracks: list[SimpleTrack] = []

    parent: Optional["Library"] = None
    children: list["Library"] = []

    def add_child(self, node: "Library"):
        self.children.append(node)

    def get_top_tracks(self, top=20):
        trs = [f"{tr.artist.name} - {tr.name}" for tr in self.tracks]
        return trs[:top] if len(trs) >= top else trs

    def get_top_artists(self, top=20):
        # go through the list of artists
        artists = [art.name for art in self.artists]

        if len(artists) >= top:
            return artists[top:]

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
        
        items = list(arts.items())
        items.sort(key=lambda a:a[1])
        items = items[-1*(top-len(artists)) : ] \
                    if len(items) > top-len(artists) \
                    else items
        artists.extend([item[0] for item in items])
        return artists


class SimpleUser(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    display_name: str
    music_model: Optional[MusicModel] = None
    ext_ids: ExternalIDs = ExternalIDs()

    @classmethod
    def get_or_create(cls, data: dict):
        return cls(**data)


class User(SimpleUser):
    email: Optional[EmailStr] = None
    
    #hash of email
    simple_id: Optional[str] = None
    first_login: Optional[str] = None
    last_login: Optional[str] = None
    num_logins: Optional[int] = 0
    sessions: Optional[list[str]] = []
    lib: Optional[Library] = None
    lib_extended: Optional[Library] = None
    thumb_url: Optional[str] = None

    @field_validator('first_login','last_login')
    @classmethod
    def validate_year(cls, v: str) -> str:
        datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
        return v    

# class Session(BaseModel):
#     user_simple_id: str
#     simple_id: str
#     time: datetime.datetime

class ProgState(BaseModel):
    VERSION: str
    PERSIST_USER_LIB: str
    SPOTIFY_KEY: dict
    REPLICATE_KEY: str
    END_OF_LIFE: str
    WEBSITE: Optional[str] = None
    LATEST_NEWS: Optional[str] = None
    FEEDBACK_URL: Optional[str] = None

    # @classmethod
    # def load_setup(cls, setup: dict) -> 'ProgState':



