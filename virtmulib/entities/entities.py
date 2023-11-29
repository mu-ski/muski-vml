from abc import ABC
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

class VMLAgent(BaseModel, ABC):
	id: int = None
	name: str = None
	
class User(VMLAgent):
	email: EmailStr = None
	id_at_source: str = None
	source: str = None

class Artist(VMLAgent):
	music_brainz_id: UUID4 = None
	active_from: datetime = None
	active_to: datetime = None

class AIAgent(VMLAgent):
	unique_model_name: str

class VMLItem(BaseModel, ABC):
	id: int = None	
	title: str
	pass

class Genre(VMLItem):
	music_brainz_id: UUID4 = None

class Album(VMLItem):
	music_brainz_id: UUID4 = None
	release_date: datetime = None
	artist: list[Artist]
	release_type: str

class Playlist(VMLItem):
	curator: VMLAgent

class UserLibrary(VMLItem):
	owner: User
	artists: list[Artist]
	playlists: list[Playlist]
	albums: list[Album]

class Track(VMLItem):
	artist: list[Artist]
	release_date: datetime
	label: str = None