import abc
from abc import ABC
from pydantic import BaseModel, EmailStr
from enum import IntEnum

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class OnLoader(BaseModel, ABC):	
	@abc.abstractmethod
	def login_signup() -> EmailStr:
		pass

class OnLoaderEnum(IntEnum):
	spotify = 1

class SpotifyOnLoader(OnLoader):
	def login_signup():
		# scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
		#   'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
		#   'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
		#   'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
		#   'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
		#   'playlist-read-private', 'playlist-modify-public']

		scopes = ['user-read-email', 'user-follow-read', 'user-library-read',
					'streaming', 'user-top-read', 'playlist-modify-public']

		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))
		user = sp.current_user()
		return user['email']