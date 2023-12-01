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
	_t: time = None
	_cnt: int = 0


	def _c(self, func, params):
		"""Routing all the API calls through this for easily  managing rate limits"""
		if self._t is None:
			self._t = time.time()
		self._cnt += 1
		#print(self._cnt)
		return func(**params)


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
			id_at_source=us.get('id'),
			source=SourcesEnum.spotify)
		return self._user.name


	def get_user_data(self) -> None:
		self.get_playlists()


	def get_playlists(self) -> list[Playlist]:
		pls_shallow = self._get_playlists_shallow()

		#pls_deep = self._get_tracklist_of_playlist(pl)
		pls_deep = [self._insert_tracklist_into_playlist(p) for p in pls_shallow]
		
		#TODO: if playlist exists load it instead
		
		print(pls_deep[0].model_dump_json(exclude_defaults=True))
		
		#pl_obj = self._get_playlist_as_obj(pl_dict)


	def _get_playlists_shallow(self) -> list[Playlist]:
		playlists = []
		for offset in range(0, 2000, 50):
			res = self._c(
					self._sp.current_user_playlists, 
					{'limit':50, 'offset':offset}
				)
			playlists.extend(
				[self._format_as_playlist_shallow(i) for i in res.get('items')]
			)
		return playlists

	def _format_as_playlist_shallow(self, item: str) -> Playlist:
		pl = {}
		pl['name'] = item.get('name')
		pl['description'] = item.get('description')
		pl['id_at_source'] = item.get('id')
		pl['source'] = SourcesEnum.spotify

		#TODO: if creator exists, load object rather than create
		pl['creator'] = Person(
			name = item.get('owner').get('display_name'),
			id_at_source=item.get('owner').get('id'),
			source=SourcesEnum.spotify
		)
		return Playlist(**pl)

	def _insert_tracklist_into_playlist(self, playlist: Playlist) -> Playlist:
		tr_ls = []
		fields = 'items(track(' + \
						'external_ids(isrc,upc),'+ \
						'id,' + \
						'name,' + \
						'album(release_date,name,id),' + \
						'artists(name, id)))'
		
		for offset in range(0, 2000, 100):
			res = self._c(
				self._sp.playlist_items,
					{'playlist_id': playlist.id_at_source, 
					'fields': fields, 
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

	def _format_as_track(self, res: dict) -> tuple[Track, Album]:
		arts = res.get('artists')
		artist = self._format_as_artist(arts[0])
		artist_sec = self._format_as_artist(arts[1]) if len(arts) > 1 else None

		#TODO: if album exists, load object rather than create
		al = res.get('album')
		alb = Album(
				name=al.get('name'),
				date=SimpleDate(al.get('release_date')).dt,
				artist=artist,
				id_at_source=al.get('id'),
				source=SourcesEnum.spotify)
		
		# Albums of tracks of playlists are not stricly part of the users lib, 
		# call it "extended lib" if you may. Anyway, we should handle it differently
		self._albums.append(alb)	
		
		# TODO: spotify uses the album date as track date, but this is not precise.
		# Query external source for track date
		tr=Track(
				name=res.get('name'),
				artist=artist,
				artist_sec=artist_sec,
				date=alb.date,
				spotify_id=res.get('id')
			)

		if (eid := res.get('external_ids')) is not None:
			tr.id_upc = eid.get('upc')
			tr.id_isrc = eid.get('isrc')

		alb.tracklist.append(tr)
		
		return tr

	def _format_as_artist(self, art: dict) -> Artist:
		return Artist(
			id_at_source=art.get('id'), 
			source=SourcesEnum.spotify,
			name=art.get('name'))

	def get_albums(self) -> list[Album]:
		pass
	
	def get_tracks(self) -> list[Track]:
		pass

	def get_artists(self) -> list[Artist]:
		pass


#Get Tracks' Audio Features
# Get audio features for multiple tracks based on their Spotify IDs.