import abc
from abc import ABC
from pydantic import BaseModel, EmailStr
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

class OnLoaderAuthError(Exception):
	"User-defined exception class to wrap auth errors of onloaders."
	pass

class OnLoader(BaseModel, ABC):	
	"Abstract class interface for onloaders."

	@abc.abstractmethod
	def login_signup() -> EmailStr:
		"Fuction to implement the login onto the onloader service."
		pass

class SpotifyOnLoader(OnLoader, arbitrary_types_allowed=True):
	sp: spotipy.Spotify = None

	def login_signup(self):
		scopes = ['user-read-email', 'user-library-read', 'streaming',
					'user-top-read', 'playlist-modify-public']

		try:
			self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))
		except SpotifyOauthError as error:
			raise OnLoaderAuthError(str(error))

		user = self.sp.current_user()
		return user['email']

	def get_user_data(self) -> None:
		if self.sp is None:
			self.login_signup()

		print()
		print('User Followed Artists')
		print(self.sp.current_user_followed_artists())
		
		print()
		print('User Followed Playlists')
		print(self.sp.current_user_playlists())

		print()
		print('User Saved albums')
		print(self.sp.current_user_saved_albums())

		print()
		print('User save tracks')
		print(self.sp.current_user_saved_tracks())

		print()
		print('User top artists')
		print(self.sp.current_user_top_artists())

		print()
		print('User top tracks')
		print(self.sp.current_user_top_tracks())
		

		#current_user_followed_artists


