import os
import logging
from hashlib import blake2b
import json
import pkgutil
from datetime import datetime

#from .frameworks_drivers import CloudDB
from .frameworks_drivers.firebase import FirebaseDBLogger
from virtmulib.applogic.onload.spotify import OnLoadSpotify
import virtmulib.applogic.gateway as usecases
from . import setup_app
from .adapters import cli
import virtmulib.applogic.offload.spotify as offload_spotify
from .entities import User, MusicModel

from virtmulib.applogic import ai_playlister

def get_user_email_hash(email):
    return blake2b(
                key=bytes(email, 'utf-8'),
                digest_size=10
            ).hexdigest()


def prog_logic():
    db = FirebaseDBLogger()

    user = None
    user_db = None
    playlist_req = None
    spotipy_cache = pkgutil.get_data('',".cache")
    
    # if user has previously logged-in from this device (a .cache file would exist)
    if spotipy_cache:
        user = usecases.login_singup_user(OnLoadSpotify)
        email_hash = get_user_email_hash(user.email)
        user_db = db.get(f'user/{email_hash}')[0]
        
    
    if user_db:
        cli.emit(">> Welcome back to 🎶Muski🎶 😊... Glad to see you return for another round!")
        if user_db.num_logins >= 2:
            print('Unfortunatley, due to limited (free) AI-servers we are using right now,' \
                    'we had to limit each user to two sessions.' \
                    'We are working on a more permanenet solution for our next release.', inpt=False)
            return
        playlist_req = cli.query_returning_user()
    else:
        cli.greet()
        cli.emit(">> Analyzing your listening habits... This can take up to a minute, please be patient 😊...")

        # load_user_library
        #user = usecases.get_user_data(OnLoadSpotify)
        user = usecases.login_singup_user(OnLoadSpotify)
        
        user.first_login = datetime.now().isoformat()
        
        email_hash = get_user_email_hash(user.email)
        #db.set(user.lib.model_dump(exclude_defaults=True), f'lib/{email_hash}')
        
        # get_top_x
        #top_artists = user.lib.get_top_artists(top=10)
        #top_tracks = user.lib.get_top_tracks(top=10)

        # Query user 
        answers = cli.query_user()
        line1 = f"Songs from my library: {top_tracks}"
        line2 = f"Artists from my library: {top_artists}"
        line3 = f"What music means to me: {answers[0]}"
        line4 = f"What music I like: {answers[1]}"
        line5 = f"What music I dislike: {answers[2]}"
        playlist_req  = f"Playlist request: {answers[3]}"

        text_background = f"{line1}\n{line2}\n{line3}\n{line4}\n{line5}"        

        user.music_model = MusicModel(
                            text_background=user_background,
                            top_artists=top_artists,
                            top_tracks=top_tracks)

    
    query = f"{user.music_model.text_background}\n{playlist_req}"

    # query AI
    val = None
    # import contextlib
    # with contextlib.redirect_stdout(os.devnull):
    #     val = ai_playlister.inference(query)
    val = 1

    if val:
        # title, playlist = val
        # make playlist
        # pl = offload_spotify.make_playlist(title, playlist)
        pl = 1
        if pl:
            cli.emit(f"Voilà! Your playlist '{title}' is ready, run check your spotify!")
        else:
            cli.emit(f"Sorry 😅, it seems something went wrong from our side, we have reported this problem and will fix it ASAP. Please try again tomorrow!")
    else:
        print('Due to user excitement and usage, the limit of the (free) AI-server we use has been completed. We are working on a more permanenet solution at the moment.')

    # update user data
    # write session 
    # say bye


if __name__ == '__main__':

    setup_app.setup_logging_env()

    logger = logging.getLogger(__name__)
    
    #setup_app.write_new_prog_state()
    setup_app.load_prog_state()
    
    logger.info("Program started")

    prog_logic()

    logger.info("Program finished")
