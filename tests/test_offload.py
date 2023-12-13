
from virtmulib.applogic.offload.spotify import make_playlist

def test_get_playlist_offload_spotify():
    l= ["The Residents - Don't Be Cruel", "The Residents - Jailhouse Rock", "The Residents - Viva Las Vegas",
        "The Residents - Pop Will Eat Itself", "The Residents - The Aging Musician"]
    make_playlist(l)

