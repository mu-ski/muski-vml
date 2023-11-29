import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyPKCE, CacheFileHandler

from virtmulib.applogic.onloader import OnLoader, OnLoaderEnum
from virtmulib.entities import Playlist, User, Track, Album, Artist

class SpotifyOnLoader(OnLoader, arbitrary_types_allowed=True):
	_sp: spotipy.Spotify = None
	_user: User = None

	def login_signup(self):
		scopes = ['user-library-read', 'user-follow-read', 'user-top-read',
					'playlist-modify-public', 'playlist-read-private']
		try:
			self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))
		except SpotifyOauthError as error:
			raise OnLoaderAuthError(str(error))
		us = self._sp.me()
		self._user = User(
			email=us.get('email'),
			name=us.get('display_name'),
			id_at_source=us.get('id'),
			source=OnLoaderEnum.Spotify)
		return self._user.name

	def get_user_data(self) -> None:
		if self._sp is None:
			self.login_signup()

		self._get_playlists()

	def _get_playlists(self) -> list[Playlist]:
		playlists = []
		for offset in range(0, 2000, 50):
			res = self._sp.current_user_playlists(limit=50, offset=offset)
			for r in res.get('items'):
				o = r.get('owner')
				id = o.get('id')
				u = self._user
				if o.get('type') == "user" and id != self._user.id_at_source:
					u = User(
						id_at_source=id, 
						name=o.get('display_name'), 
						source=OnLoaderEnum.Spotify)
				pl = Playlist(title=r.get('name'), curator=u)
				playlists.append(pl)
		return playlists

	def _get_playlist_tracks(self) -> list[Track]:
		pass

	def _get_albums(self) -> list[Album]:
		pass

	def _get_liked_tracks(self) -> list[Track]:
		pass

	def _get_top_artist(self) -> list[Artist]:
		pass

	def _get_top_tracks(self) -> list[Track]:
		pass

	def _get_followed_artists(self) -> list[Artist]:
		pass
		
# current_user_saved_albums(limit=20, offset=0)
# current_user_saved_tracks(limit=20, offset=0)
# current_user_top_artists(limit=20, offset=0, time_range='long_term')
# current_user_top_tracks(limit=20, offset=0, time_range='long_term')

# current_user_followed_artists(limit=20, after=None)

