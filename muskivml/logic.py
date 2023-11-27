from os import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = environ.get('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = environ.get('SPOTIFY_REDIRECT_URI')

class OnLoader:
	def login_with_spotify():
		# scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
		#   'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
		#   'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
		#   'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
		#   'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
		#   'playlist-read-private', 'playlist-modify-public']

		scopes = ['user-read-email', 'user-follow-read', 
				'user-library-read', 'streaming', 'user-top-read', 'playlist-modify-public']

		# L'auth flow si basa sul eseguire questo codice
		# Andare alla redirect uri e ricopiare l'intera url nel prompt in console
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
													   client_secret=CLIENT_SECRET,
													   redirect_uri=REDIRECT_URI,
													   scope=scopes))
		return sp.current_user()['email']
		
OnLoader.login_with_spotify()