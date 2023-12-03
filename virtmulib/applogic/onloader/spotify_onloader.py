import json
import time
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyPKCE, CacheFileHandler

from virtmulib.applogic.onloader import OnLoader
from virtmulib.entities import *

TEST = True

SCOPES = ['user-library-read', 'user-follow-read', 'user-top-read',
		'playlist-modify-public', 'playlist-read-private']

class SpotifyOnLoader(OnLoader, arbitrary_types_allowed=True):
	_sp: spotipy.Spotify = None
	_user: User = None
	_albums: list[Album] = []
	_tracks: list[Track] = []
	_artists: list[Artist] = []
	_playlists: list[Playlist] = []
	_albums_to_read: list[Album] = []
	_tracks_to_read: list[Track] = []
	_artists_to_read: list[Artist] = []
	_playlists_to_read: list[Playlist] = []

	_t: time = None
	_cnt: int = 0


	def _c(self, func, inp=None, params=None):
		"""Routing all the API calls through this for easily  managing rate limits"""
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
				pass
				#return func(inp, **params)
		#return func(**params)


	def model_post_init(self, __context):
		self.login_signup()


	def login_signup(self):
		if self._sp is not None and self._user is not None:
			return self._user.name
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
				ext_ids=ExternalIDs(spotify=us.get('id'))
			)
		return self._user.name


	def get_user_data(self) -> None:
		self.get_playlists()
		
		print()
		print()
		
		self.get_albums()


	def get_playlists(self) -> list[Playlist]:
		pls_shallow = self._get_user_playlists_shallow()

		#pls_deep = self._get_tracklist_of_playlist(pl)
		
		if TEST:
			pls_deep = self._insert_tracklist_into_playlist(pls_shallow[0])
		else:
			pls_deep = [self._insert_tracklist_into_playlist(p) for p in pls_shallow]
		
		#TODO: if playlist exists load it instead
		
		print(pls_deep.model_dump_json(exclude_defaults=True))
		
		#pl_obj = self._get_playlist_as_obj(pl_dict)


	def get_albums(self) -> list[Album]:
		albs = self._get_albums()
		print(albs[0].model_dump_json(exclude_unset=True, exclude_defaults=True, exclude_none=True))


	def _get_albums(self) -> list[Album]:
		albs = []
		for offset in range(0, 2000, 20):
			res = self._c(
					self._sp.current_user_saved_albums,
					params={'limit':20, 'offset':offset}
				)
			albs.extend([self._read_album(alb) for alb in res.get('items')])
		return albs
			
	def _read_album(self, item: dict) -> Album:
		if 'album' in item.keys():
			item = item.get('album')
		alb = {}
		
		arts = item.get('artists')
		alb['artist'] = self._format_as_artist(arts[0])
		alb['artist_sec'] = self._format_as_artist(arts[1]) if len(arts) > 1 else None

		alb['release_type'] = ReleaseTypeEnum.get_release_enum_by_name(item.get('album_type'))
		alb['label'] = item.get('label')
		alb['name'] = item.get('name')
		alb['date'] = SimpleDate(item.get('release_date')).dt

		imgs = item.get('images')
		alb['thumb'] = imgs[0].get('url') if imgs is not None and len(imgs) != 0 else None

		alb_obj = self._create_or_load_album(alb)
		
		if alb_obj.tracklist == []:
			items = item.get('tracks').get('items')
			#print(json.dumps())	
			trklst = [self._format_as_track(itm, alb_obj) for itm in items]
			#trklst = self._get_a_list_of_tracks(item.get('tracks'))
			alb_obj.tracklist = trklst

		return alb_obj
		

	def _get_a_list_of_tracks(self, tracks: list) -> list[Track]:
		if 'items' in tracks.keys():
			tracks = tracks['items']
		
		tr_ids = [tr.get('id') for tr in tracks.get('items')]
		trs_data = self._c(self._sp.tracks, inp=tr_ids).get('tracks')

		return [self._create_or_load_track(tr_data) for tr_data in trs_data]


	def _get_user_playlists_shallow(self) -> list[Playlist]:
		playlists = []
		for offset in range(0, 2000, 50):
			res = self._c(
					self._sp.current_user_playlists, 
					params={'limit':50, 'offset':offset}
				)
			playlists.extend(
				[self._format_as_playlist_shallow(i) for i in res.get('items')]
			)
			if TEST:
				return playlists
		return playlists

	def _format_as_playlist_shallow(self, item: str) -> Playlist:
		pl = {}
		pl['name'] = item.get('name')
		pl['description'] = item.get('description')
		pl['ext_ids'] = {'spotify': item.get('id')}
		
		imgs = item.get('images')
		pl['thumb'] = imgs[0].get('url') if imgs is not None and len(imgs) != 0 else None

		pl['creator'] = self._format_as_user({
							'name': item.get('owner').get('display_name'),
							'ext_ids': ExternalIDs(spotify=item.get('owner').get('id'))
						})

		return Playlist(**pl)

	def _insert_tracklist_into_playlist(self, playlist: Playlist) -> Playlist:
		tr_ls = []
		for offset in range(0, 2000, 100):
			res = self._c(
				self._sp.playlist_items,
				params={'playlist_id': playlist.ext_ids.spotify, 
						'limit': 100, 
						'offset': offset, 
						'additional_types': ('track',)
					}
				)
			tracks = res.get('items')
			tracks = [self._format_as_track(tr.get('track')) for tr in tracks]
			tr_ls.extend(tracks)
		playlist.tracklist = tr_ls
		return playlist

	def _format_as_track(self, res: dict, alb=None) -> Track:
		tr = {}
		tr['name'] = res.get('name')
		arts = res.get('artists')
		tr['artist'] = self._format_as_artist(arts[0])
		tr['artist_sec'] = self._format_as_artist(arts[1]) if len(arts) > 1 else None

		tr['ext_ids']=ExternalIDs(spotify=res.get('id'))
		if 'external_ids' in res.keys():
			tr['ext_ids'].upc = res.get('external_ids').get('upc')
			tr['ext_ids'].isrc = res.get('external_ids').get('isrc')
		
			# alb = self._read_album(res.get('album'))
			# Albums of tracks of playlists are not stricly part of the users lib, 
			# call it "extended lib" if you may. Anyway, we should handle it differently
			#self._add_to_extended_library(alb)
	
		tr = self._create_or_load_track(tr)
		
		if alb is None and 'album' in res.keys():
			al = res.get('album')
			alb = Album(
						name=al.get('name'),
						artist=tr.artist,
						ext_ids=ExternalIDs(spotify=al.get('id')),
						date=SimpleDate(al.get('release_date')).dt
					)

			if alb.date < tr.date:
				tr.date = alb.date

			tr.albums.append(alb)

			self._add_to_to_read(alb)

		# # TODO: spotify uses the album date as track date, but this is not precise.
		# # Query external source for track date
		# tr=Track(
		# 		name=res.get('name'),
		# 		artist=artist,
		# 		artist_sec=artist_sec,
		# 		date=date,
		# 		ext_ids=ExternalIDs(spotify=res.get('id'))
		# 	)
		return tr

	def _format_as_artist(self, item:dict) -> Artist:
		return self._create_or_load_artist({
			'name': item['name'],
			'ext_ids': ExternalIDs(spotify=item.get('id'))
		})

	def _format_as_user(self, item: dict) -> User:
		return self._create_or_load_user(item)
	
	def _add_to_extended_library(self, alb: Album) -> None:
		# TODO: Add a cache and only append if not in cache
		self._albums.append(alb)

	def _add_to_to_read(self, obj: VMLThing) -> None:
		# TODO: Add a cache and only append if not in cache
		if type(obj) == Album:
			self._albums_to_read.append(obj)
		elif type(obj) == Artist:
			self._artists_to_read.append(obj)
		elif type(obj) == Playlist:
			self._playlists_to_read.append(obj)
		elif type(obj) == Track:
			self._tracks_to_read.append(obj)



	def _create_or_load_track(self, data: dict) -> Track:
		return Track(**data)

	def _create_or_load_album(self, data: dict) -> Album:
		return Album(**data)


	def _create_or_load_artist(self, data: dict) -> Artist:
		return Artist(**data)

	def _create_or_load_user(self, data: dict) -> User:
		return User(**data)

	def _create_or_load_playlist(self, data: dict) -> Playlist:
		return playlist(**data)

	def get_tracks(self) -> list[Track]:
		pass

	def get_artists(self) -> list[Artist]:
		pass


#Get Tracks' Audio Features
# Get audio features for multiple tracks based on their Spotify IDs.