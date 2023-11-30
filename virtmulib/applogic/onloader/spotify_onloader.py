import json
import spotipy
import time
from datetime import date
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyPKCE, CacheFileHandler

from virtmulib.applogic.onloader import OnLoader, OnLoaderEnum
from virtmulib.entities import Playlist, User, Track, Album, Artist, Genre

SCOPES = ['user-library-read', 'user-follow-read', 'user-top-read',
		'playlist-modify-public', 'playlist-read-private']

class SpotifyOnLoader(OnLoader, arbitrary_types_allowed=True):
	_sp: spotipy.Spotify = None
	_user: User = None
	_t: time = None
	_cnt: int = 0

	def _c(self, func, params):
		if self._t is None:
			self._t = time.time()
		self._cnt += 1
		#print(self._cnt)
		return func(**params)

	def login_signup(self):
		try:
			self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))
		except SpotifyOauthError as error:
			raise OnLoaderAuthError(str(error))
		us = self._sp.me()
		# TODO: when using persistence, first check if user exists 
		# 		if yes, then retrieve object, else create new obj
		self._user = User(
			email=us.get('email'),
			name=us.get('display_name'),
			id_at_source=us.get('id'),
			source=OnLoaderEnum.Spotify)
		return self._user.name

	def get_user_data(self) -> None:
		if self._sp is None or self._user is None:
			self.login_signup()
		self._get_playlists()
		print(self._user.library.model_dump_json(exclude_defaults=True))

	def _get_albums(self) -> list[Album]:
		pass
	
	def _get_tracks(self) -> list[Track]:
		return self._get_liked_tracks().extend(
				self._get_top_tracks())

	def _get_artists(self) -> list[Artist]:
		return self._get_top_artist().extend(
			self._get_followed_artists())

	def _get_playlists(self) -> None:
		playlists = []
		for offset in range(0, 2000, 50):
			#res = self._sp.current_user_playlists(limit=50, offset=offset)
			res = self._c(self._sp.current_user_playlists, {'limit':50, 'offset':offset})
			for r in res.get('items'):
				pl = self._get_one_playlist(r)
				self._user.library.add(pl)

	def _get_one_playlist(self, item) -> Playlist:
		o = item.get('owner')
		id = o.get('id')
		u = self._user
		if o.get('type') == "user" and id != self._user.id_at_source:
			u = User(
				id_at_source=id, 
				name=o.get('display_name'), 
				source=OnLoaderEnum.Spotify)
		trlst = self._get_playlist_tracks(item.get('id'))
		pl = Playlist(
			name=item.get('name'), 
			creator=u, 
			description=item.get('description'),
			tracklist=trlst)
		return pl

	#Get Several Albums (max 20)
	#Get Several Artists (max 50)
	#Get Several Tracks  (max 50)
	
	def _get_playlist_tracks(self, playlist_id) -> list[Track]:
		ls = []
		fields = 'items(track(external_ids(isrc),id,name,album(release_date,name,id), artists(name, id)))'
		for offset in range(0, 2000, 100):
			res = self._c(
				self._sp.playlist_items,
					{'playlist_id': playlist_id, 
					'fields': fields, 
					'limit': 100, 
					'offset': offset, 
					'additional_types': ('track',)
					}
				)
			# res = self._sp.playlist_items(
			# 		playlist_id=playlist_id, 
			# 		fields=fields, 
			# 		limit=100, 
			# 		offset=offset, 
			# 		additional_types=('track',))
			ls.extend(self._get_list_of_tracks(res))
		return ls
		

	def _get_list_of_tracks(self, res) -> list[Track]:
		trls = []
		res = res.get('items')
		for r in res:
			trls.append(self._get_track(r))
		return trls

	def _get_track(self, res) -> Track:
		res = res.get('track')
		arts = res.get('artists')
		art = arts[0]
		artist = Artist(spotify_id=art.get('id'), name=art.get('name'))
		self._user.library.add(artist)
		
		artist_sec = None
		if len(arts) > 1:
			artist_sec = Artist(
							spotify_id=arts[1].get('id'),
							name=arts[1].get('name'))
			self._user.library.add(artist_sec)
		
		alb = res.get('album')
		al = Album(
				name=alb.get('name'),
				date=self._get_str_date_as_date_obj(alb.get('release_date')),
				artist=artist,
				spotify_id=alb.get('is'))
		
		self._user.library.add(al)

		# TODO: spotify uses the album date as track date, but this is not precise. Query external source for track date
		tr=Track(
			name=res.get('name'), 
			artist=artist, 
			secondary_artist=artist_sec, 
			date=al.date, 
			spotify_id=res.get('id'), 
			isrc_id=res.get('external_ids').get('isrc'))

		al.tracklist.append(tr)

		self._user.library.add(tr)
		
		return tr

	def _get_str_date_as_date_obj(self, dt) -> date:
		lis = [int(i) for i in dt.split('-')]
		if len(lis) < 3:
			default_date = [1900, 1, 1]
			lis.extend(default_date[len(lis):])
		return date(*lis)


	def _get_album_tracks(self) -> list[Track]:
		return []

	def _get_genres(self) -> list[Genre]:
		return []

	def _get_liked_tracks(self) -> list[Track]:
		pass

	def _get_top_tracks(self) -> list[Track]:
		pass

	def _get_top_artist(self) -> list[Artist]:
		pass

	def _get_followed_artists(self) -> list[Artist]:
		pass
		
# current_user_saved_albums(limit=20, offset=0)
# current_user_saved_tracks(limit=20, offset=0)
# current_user_top_artists(limit=20, offset=0, time_range='long_term')
# current_user_top_tracks(limit=20, offset=0, time_range='long_term')

# current_user_followed_artists(limit=20, after=None)

