import json
import time
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError, SpotifyPKCE, CacheFileHandler

from virtmulib.applogic.onloader import OnLoader
from virtmulib.entities import *

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
				# TODO: need to check if this condition ever occurs
				pass


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
		pl = self.get_playlists()

		print(pl[0].model_dump_json(exclude_defaults=True))

		albs = self.get_albums()

		print(albs[0].model_dump_json(exclude_defaults=True))

		trs = self.get_tracks()

		print(trs[0].model_dump_json(exclude_defaults=True))

		self.get_artists()


	def get_tracks(self) -> list[Track]:		
		tracks = self._get(self._sp.current_user_top_tracks, self._format_as_track)
		tracks.extend(self._get(self._sp.current_user_saved_tracks, self._format_as_track))
		return tracks

	def get_albums(self) -> list[Album]:
		return self._get(self._sp.current_user_saved_albums, self._format_as_album)

	def get_playlists(self) -> list[Playlist]:
		return self._get(self._sp.current_user_playlists, self._format_as_playlist)


	def get_artists(self) -> list[Artist]:
		return self._get(self._sp.current_user_top_artists, self._format_as_artist)

	def get_related_artists(self, art_id: str) -> list[Artist]:
		# artist_related_artists(artist_id)
		pass

	def _get(self, func1, func2) -> list[VMLThing]:
		items = []
		for offset in range(0, 2000, 20):
			res = self._c(
					func1,
					params={'limit': 20, 'offset': offset}
				)
			if res['items'] == [] and res['next'] is None:
				break
			items.extend([func2(item) for item in res.get('items')])
		return items


	def _format_as_album(self, item: dict) -> Album:
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
		
		if 'genres' in item.keys():
			grs = [Genre(name=g) for g in item['genres']]
			alb['genres'] = grs

		alb_obj = self._create_or_load_album(alb)
		
		if alb_obj.tracklist == []:
			items = item.get('tracks').get('items')
			trklst = [self._format_as_track(itm, alb_obj) for itm in items]
			alb_obj.tracklist = trklst

		return alb_obj
		

	def _get_a_list_of_tracks(self, tracks: list) -> list[Track]:
		if 'items' in tracks.keys():
			tracks = tracks['items']
		
		tr_ids = [tr.get('id') for tr in tracks.get('items')]
		trs_data = self._c(self._sp.tracks, inp=tr_ids).get('tracks')

		return [self._create_or_load_track(tr_data) for tr_data in trs_data]


	def _format_as_playlist(self, item: str) -> Playlist:
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

		pl_o = self._create_or_load_playlist(pl)
		self._insert_tracklist_into_playlist(pl_o)
		return pl_o


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
			if res['items'] == [] and res['next'] is None:
				break
			tracks = res.get('items')
			tracks = [self._format_as_track(tr) for tr in tracks]
			tr_ls.extend(tracks)
		playlist.tracklist = tr_ls
		return playlist


	def _format_as_track(self, res: dict, alb=None) -> Track:
		if 'track' in res.keys():
			res = res.get('track')

		tr = {}
		tr['name'] = res.get('name')
		arts = res.get('artists')
		tr['artist'] = self._format_as_artist(arts[0])
		tr['artist_sec'] = self._format_as_artist(arts[1]) if len(arts) > 1 else None

		tr['ext_ids']=ExternalIDs(spotify=res.get('id'))
		if 'external_ids' in res.keys():
			tr['ext_ids'].upc = res.get('external_ids').get('upc')
			tr['ext_ids'].isrc = res.get('external_ids').get('isrc')
			
		if 'images' in res.keys():
			tr['thumb'] = res.get('images')[0].get('url')

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
		return tr


	def _format_as_artist(self, item: dict) -> Artist:
		art = {
			'name': item['name'],
			'ext_ids': ExternalIDs(spotify=item.get('id'))
		}
		if 'genres' in item.keys():
			grs = [Genre(name=g) for g in item['genres']]
			art['genres'] = grs
		if 'images' in item.keys():
			art['thumb'] = item['images'][0]['url']
		return self._create_or_load_artist(art)


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
		return Playlist(**data)




#Get Tracks' Audio Features
# Get audio features for multiple tracks based on their Spotify IDs.