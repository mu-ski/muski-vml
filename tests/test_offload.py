
from virtmulib.applogic.offload.spotify import make_playlist




# def test_get_playlist_offload_spotify():
#     l= ["The Residents - Don't Be Cruel", "The Residents - Jailhouse Rock", "The Residents - Viva Las Vegas",
#         "The Residents - Pop Will Eat Itself", "The Residents - The Aging Musician"]
#     make_playlist(l, "The Residents (II)")

def test_get_playlist_offload_spotify_2():
    l = ["Fela Kuti - Zombie", "Baba Maal - Yela", "Caetano Veloso - Terra", 
        "Herbie Hancock - Watermelon Man", "Ali Farka Toure - Tinariwen", 
        "The Cinematic Orchestra - To Build a Home", "Mulatu Astatke - Yegelle Tezeta",
        "Khruangbin - Maria También", "BADBADNOTGOOD - Time Moves Slow", "Richard Bona - Mbemba"]
    make_playlist(l, "Sunny Decemeber Sunday Playlist")
