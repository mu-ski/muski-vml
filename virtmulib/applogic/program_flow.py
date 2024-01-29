import os
from hashlib import blake2b
import json
import pkgutil
from datetime import datetime


from virtmulib.frameworks_drivers.firebase import FirebaseDBLogger
from virtmulib.applogic.onload.spotify import OnLoadSpotify
import virtmulib.applogic.gateway as usecases
from virtmulib.adapters import cli
import virtmulib.applogic.offload.spotify as offload_spotify
from virtmulib.entities import User, MusicModel

from virtmulib.applogic import ai_playlister

TEST = False


def get_user_email_hash(email):
    return blake2b(key=bytes(email, "utf-8"), digest_size=10).hexdigest()


# def store_user_id(user_id):
#     os.environ['USER_ID'] = user_id

# def get_user_id():
#     return os.environ['USER_ID']


def store_user_data(user: User, playlist_title, playlist):
    db = FirebaseDBLogger()
    user_id = get_user_email_hash(user.email)

    user.last_login = datetime.now().isoformat()
    if user.first_login is None:
        user.first_login = user.last_login

    user.num_logins += 1

    if playlist_title and playlist:
        db.set(playlist, f"playlists/{user.display_name}/{playlist_title}")

    db.set(
        user.model_dump(exclude_defaults=True, exclude={"lib", "lib_extended"}),
        f"users/{user.display_name}",
    )

    if user.lib:
        db.set(user.lib.model_dump(exclude_defaults=True), f"lib/{user.display_name}")


def prog_logic():
    db = FirebaseDBLogger()

    user = None
    user_db = None
    playlist_req = None
    spotipy_cache = pkgutil.get_data("", ".cache")

    # # if user has previously logged-in from this device (a .cache file would exist)
    # if spotipy_cache:
    #     user = usecases.login_singup_user(OnLoadSpotify)
    #     #user_id = get_user_email_hash(user.email)
    #     user_db = db.get(f'users/{user.display_name}')[0]
    #     #store_user_id(user_id)

    cli.greet()
    cli.emit(
        ">> Analyzing your listening habits... This can take up to a minute, please be patient 😊..."
    )

    # load_user_library
    user = usecases.login_singup_user(OnLoadSpotify)
    user_db = db.get(f"users/{user.display_name}")[0]

    # if no base user data exists in the DB, then get it-
    if not user_db:
        user = usecases.get_user_data(OnLoadSpotify)

        # get_top_x
        top_artists = user.lib.get_top_artists(top=10)
        top_tracks = user.lib.get_top_tracks(top=10)

        # Query user
        answers = cli.query_user()
        line1 = f"Songs from my library: {top_tracks}"
        line2 = f"Artists from my library: {top_artists}"
        line3 = f"What music means to me: {answers[0]}"
        line4 = f"Music I avoid / dislike: {answers[1]}"

        text_background = f"{line3}\n{line4}"

        user.music_model = MusicModel(
            text_background=text_background,
            top_artists=top_artists,
            top_tracks=top_tracks,
        )
    else:
        user = User(**user_db)
        cli.emit(">> Welcome back 😊... Glad to see you return for another round!")
        if user.num_logins >= 2:
            cli.emit(
                "Unfortunatley, due to limited (free) AI-servers we are using right now,"
                "we had to limit each user to two sessions."
                "If you really likes this and want more, tell our developer! :)"
            )
            store_user_data(user, None, None)
            return

    # Query user playlist
    playlist_req = cli.query_user_playlist()
    playlist_req = f"Playlist request: {playlist_req}"

    # print(user)
    artists = f"Artists from my library: {user.music_model.top_artists}"
    tracks = f"Songs from my library: {user.music_model.top_tracks}"

    query = f"{user.music_model.text_background}\n{artists}\n{tracks}\n{playlist_req}"

    # query AI
    val = None
    import contextlib

    if not TEST:
        val = ai_playlister.inference(query)
        # with contextlib.redirect_stdout(os.devnull):
        #    val = ai_playlister.inference(query)

    playlist_title = None
    playlist = None

    if val:
        playlist_title, playlist = val
        # make playlist
        pl_url = offload_spotify.make_playlist(playlist_title, playlist)
        if pl_url:
            cli.emit(
                f"Voilà! Your playlist '{playlist_title}' is ready, it can be accessed on: {pl_url}"
            )
        else:
            cli.emit(
                f"Sorry 😅, it seems something went wrong from our side, we have reported this problem and will fix it ASAP. Please try again tomorrow!"
            )
    else:
        print(
            "Due to user excitement and usage, the limit of the (free) AI-servers we use has been completed. We are working on a more permanenet solution at the moment."
        )

    store_user_data(user, playlist_title, playlist)
    # say bye
