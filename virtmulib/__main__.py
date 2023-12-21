import os
import logging

#from .frameworks_drivers import CloudDB
from .frameworks_drivers.firebase import FirebaseDBLogger
from virtmulib.applogic.onload.spotify import OnLoadSpotify
import virtmulib.applogic.gateway as usecases
from . import setup_app
from .adapters import cli

import virtmulib.applogic.offload.spotify as offload_spotify

from virtmulib.applogic import ai_playlister

def prog_logic():
    db = FirebaseDBLogger()
    
    cli.greet()
    cli.emit(">> Analyzing your listening habits... This can take up to a minute, please be patient 😊...")
    user = usecases.get_user_data(OnLoadSpotify)
    user_id = hash(user.email)
    user_dat = db.get(f'user/{user_id}')[0]

    # new user
    if not user_dat:

        # load_user_library
        user = usecases.get_user_data(OnLoadSpotify)
        
        # get_top_x
        top_artists = user.lib.get_top_artists(top=10)
        top_tracks = user.lib.get_top_tracks(top=10)

        # Query user 
        answers = cli.query_user()
        line1   = f"Songs from my library: {top_tracks}"
        line2   = f"Artists from my library: {top_artists}"
        line3   = f"What music means to me: {answers[0]}"
        line4   = f"What music I like: {answers[1]}"
        line5   = f"What music I dislike: {answers[2]}"
        line5   = f"Playlist request: {answers[3]}"
        query   = f"{line1}\n{line2}\n{line3}\n{line4}\n{line5}\n"


        # query AI
        val = None
        # import contextlib
        # with contextlib.redirect_stdout(os.devnull):
        #     val = ai_playlister.inference(query)
        val = 1

        if val:
            title, playlist = val
            # make playlist
            # pl = offload_spotify.make_playlist(title, playlist)
            pl = 1
            if pl is not None:
                cli.emit(f"Voilà! Your playlist '{title}' is ready, run check your spotify!")
            else:
                cli.emit(f"Sorry 😅, it seems something went wrong from our side, we have reported this problem and will fix it ASAP. Please try again tomorrow!")
        else:
            print('Due to user excitement and usage, the limit of the (free) AI-server we use has been completed. We are working on a more permanenet solution at the moment.')

        # Recommend and create playlist
        # logger.info("Successfully recommended playlist")
        # log plalylist to playlists
    # else
        # print("Welcome back")
        # if first revisit:
            # logger.info("Revisiting User")
            # simple query user
            # Recommend and create playlist
            # logger.info("Successfully recommended playlist")
            # log plalylist to playlists
        # else:
        #   tell them sorry for the user limit but each user can try twice

    # update user data
    # write session 
    # say bye



if __name__ == '__main__':

    setup_app.setup_logging_env()

    logger = logging.getLogger(__name__)
    
    setup_app.write_new_prog_state()
    setup_app.load_prog_state()
    
    logger.info("Program started")

    prog_logic()

    logger.info("Program finished")
