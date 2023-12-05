import json
import time
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyPKCE, CacheFileHandler

from virtmulib.applogic.onloader import OnLoader
from virtmulib.entities import *

TEST = True
FIRST = True
SCOPES = ['user-library-read', 'user-follow-read', 'user-top-read',
		'playlist-modify-public', 'playlist-read-private']

class SpotifyOnLoader(OnLoader, arbitrary_types_allowed=True):
	_sp: spotipy.Spotify = None
	_user: User = None
	_lib_to_read: Library = Library()
	_t: time = None
	_cnt: int = 0


	def _c(self, func, params=None, inp=None):
		"""Routing all the API calls through this for easily managing rate limits"""
		if self._t is None:
			self._t = time.time()
		self._cnt += 1
		#print(self._cnt)
		if params is None or params == {}:
			if inp is None:
				return func()
			else:
				return func(inp)
		else:
			if inp is None:
				return func(**params)
			else:
				return func(inp, **params)


	def model_post_init(self, __context):
		self.login_signup()


	def login_signup(self):
		if self._sp is not None and self._user is not None:
			return self._user.name
		try:
			self._sp = spotipy.Spotify(
							auth_manager=SpotifyOAuth(scope=SCOPES))
		except SpotifyOauthError as error:
			raise OnLoaderAuthError(str(error))
		self._user = self._format_as_user(self._sp.me())
		return self._user.name


	def get_user_data(self) -> None:
		pl = self.get_playlists()
		print(pl[0].model_dump_json(exclude_defaults=True))

		print()
		print(f'num of calls: {self._cnt}')
		self._cnt = 0
		print()


		albs = self.get_albums()
		print(albs[0].model_dump_json(exclude_defaults=True))
		
		print()
		print(f'num of calls: {self._cnt}')
		self._cnt = 0
		print()

		trs = self.get_tracks()
		print(trs[0].model_dump_json(exclude_defaults=True))

		print()
		print(f'num of calls: {self._cnt}')
		self._cnt = 0
		print()

		arts = self.get_artists()
		if len(arts) > 0:
			print(arts[0].model_dump_json(exclude_defaults=True))

		print()
		print(f'num of calls: {self._cnt}')
		self._cnt = 0
		print()


	def get_tracks(self) -> list[Track]:		
		tracks = self._get(
						self._sp.current_user_top_tracks,
						self._format_as_track
					)
		tracks.extend(
				self._get(
						self._sp.current_user_saved_tracks,
						self._format_as_track
						)
				)
		return tracks

	def get_albums(self) -> list[Album]:
		return self._get(
					self._sp.current_user_saved_albums,
					self._format_as_album
				)

	def get_playlists(self) -> list[Playlist]:
		return self._get(
					self._sp.current_user_playlists,
					self._format_as_playlist
				)

	def get_artists(self) -> list[Artist]:
		return self._get(
					self._sp.current_user_top_artists,
					self._format_as_artist
				)

	def get_related_artists(self, art_id: str) -> list[Artist]:
		# artist_related_artists(artist_id)
		pass

	def _get(self, spot_func, format_func, limit=20, inp=None) -> list[VMLThing]:
		items = []
		for offset in range(0, 2000, limit):
			res = self._c(
					spot_func,
					params={'limit': limit, 'offset': offset},
					inp=inp
				)
			if res['items'] == []: break
			items.extend([format_func(item) for item in res.get('items')])
		return items

	def _get_a_list_of_tracks(self, tracks: list) -> list[Track]:
		if 'items' in tracks.keys():
			tracks = tracks['items']
		tr_ids = [tr.get('id') for tr in tracks.get('items')]
		trs_data = self._c(
							self._sp.tracks,
							inp=tr_ids
						).get('tracks')
		return [self._create_or_load_track(tr_data) for tr_data in trs_data]


	def _format_common_fields(self, item: dict) -> dict:
		it = {}
		it['name'] = item.get('name')
		it['ext_ids'] = {'spotify': item.get('id')}
		
		if 'genres' in item.keys():
			grs = [Genre(name=g) for g in item['genres']]
			it['genres'] = grs
		
		imgs = item.get('images')
		it['thumb'] = imgs[0].get('url') if imgs is not None and len(imgs) != 0 else None

		if 'artists' in item.keys():
			arts = item.get('artists')
			it['artist'] = self._format_as_artist(arts[0])
			it['artist_sec'] = self._format_as_artist(arts[1]) if len(arts) > 1 else None
		return it


	def _format_as_album(self, item: dict) -> Album:
		if 'album' in item.keys():
			item = item.get('album')
		alb = self._format_common_fields(item)
		alb['release_type'] = ReleaseTypeEnum.get_release_enum_by_name(item.get('album_type'))
		alb['label'] = item.get('label')
		alb['date'] = SimpleDate(item.get('release_date')).dt

		alb_obj = self._create_or_load_album(alb)
		if alb_obj.tracklist == [] and 'tracks' in item.keys():
			items = item.get('tracks').get('items')
			trklst = [self._format_as_track(itm, alb_obj) for itm in items]
			alb_obj.tracklist = trklst
		return alb_obj
		

	def _format_as_playlist(self, item: dict) -> Playlist:
		pl = self._format_common_fields(item)
		pl['description'] = item.get('description')
		pl['creator'] = self._format_as_user(item.get('owner'))
		pl_o = self._create_or_load_playlist(pl)
		pl_o.tracklist = self._get(
							self._sp.playlist_items,
							self._format_as_track,
							inp=pl_o.ext_ids.spotify,
							limit=100
						)
		return pl_o


	def _format_as_track(self, res: dict, alb=None) -> Track:
		if 'track' in res.keys():
			res = res.get('track')
		tr = self._format_common_fields(res)
		if 'external_ids' in res.keys():
			tr['ext_ids']['upc'] = res.get('external_ids').get('upc')
			tr['ext_ids']['isrc'] = res.get('external_ids').get('isrc')	
		if alb is None and 'album' in res.keys():
			al = res.get('album')
			al['artist'] = tr['artist']
			alb = self._format_as_album(al)
			self._add_to_to_read(alb)
		tr = self._create_or_load_track(tr)
		if alb.date < tr.date:
			tr.date = alb.date
		return tr


	def _format_as_artist(self, item: dict) -> Artist:
		return self._create_or_load_artist(
				self._format_common_fields(item)
			)


	def _format_as_user(self, item: dict) -> User:
		return self._create_or_load_user({
						'email': item.get('email'),
						'name': item.get('display_name'),
						'ext_ids': {'spotify': item.get('id')}
						})

	def _add_to_to_read(self, obj: VMLThing) -> None:
		# TODO: Add a cache and only append if not in cache
		self._lib_to_read.add(obj)
	

#Get Tracks' Audio Features
# Get audio features for multiple tracks based on their Spotify IDs.
