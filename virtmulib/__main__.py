import os
import logging

#from .frameworks_drivers import CloudDB
from .frameworks_drivers.firebase import FirebaseDBLogger
from virtmulib.applogic.onload.spotify import OnLoadSpotify
import virtmulib.applogic.gateway as usecases
from . import setup_app
from .adapters import cli

def prog_logic():
    db = FirebaseDBLogger()
    
    user = usecases.get_user_data(OnLoadSpotify)
    user_id = hash(user.email)
    user_dat = db.get(f'user/{user_id}')

    # new user
    # if not user_dat:
    #     cli.greet()

        # # load_user_library
        # user = usecases.get_user_data(OnLoadSpotify)
        
        # # get_top_x
        # top_artists = user.lib.get_top_artists()
        # top_tracks = user.lib.get_top_tracks()

        # Query user 
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
    
    #setup_app.write_new_prog_state()
    setup_app.load_prog_state()
    
    logger.info("Program started")

    prog_logic()

    logger.info("Program finished")
