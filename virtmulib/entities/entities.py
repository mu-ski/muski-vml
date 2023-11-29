from abc import ABC
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

class VMLAgent(BaseModel, ABC):
	id: int = None
	name: str

class User(VMLAgent):
	email: EmailStr
	offloader_name: str = None
	user_offloader_id: str = None

class Artist(VMLAgent):
	music_brainz_id: UUID4 = None
	active_from: datetime = None
	active_to: datetime = None

class VMLItem(BaseModel, ABC):
	pass

class Genre(VMLItem):
	id: int = None
	title: str
	music_brainz_id: UUID4 = None

class Collection(VMLItem, ABC):
	id: int = None
	title: str
	music_brainz_id: UUID4 = None
	created_on: datetime = None
	authors: list[VMLAgent]

class Album(Collection):
	pass

class Playlist(Collection):
	pass

class UserLibrary(VMLItem):
	user: User
	artists: list[Artist]
	playlists: list[Playlist]
	albums: list[Album]