
def printn(s, empty_return=True):
    note2 = "Press enter ⏎..." if empty_return else ">> "
    print(s)
    _printn()
    inp=input(note2)
    _printn()
    return inp

def _printn(n=15, s=''):
    for i in range(0,n):
        print(s)

def greet():
    printn(" >> Welcome! I am Muski 🎶, an app to help you enjoy music again!")
    printn(" >> Muski is a tool to help you find music you enjoy.")
    printn(" >> It does that by asking you for your preferences and creating a custom-made playlist for you automatically on your spotify account.")
    printn(" >> Muski works as follows:")
    printn(" >> 1. First, you give the Muski access to your spotify: it uses your spotify data to create a new Muski account and understands what music you like.")
    printn(" >> 2. Second, you answer a couple of questions about what music means to you and your personal music preferences.")
    printn(" >> 3. Finally, the good part, you describe what kind of music you want to hear right NOW, and, viola, you will have a new playlist on your spotify.")
    printn(" >> Ready to start? 😀") 
    printn(" >> As soon as you press enter ⏎, your browser will open the spotify website, and you will be asked to allow Muski to read your data.")

def query_user():
    pass
#         Top songs: Herbie Hancock - Maiden Voyage, Laika - Praire Dog
#         What music means to me: Music is what I listen to when I need to discover new feelings and new imagination
#         Liked Music: I like many kinds of music, as long as its creative, emotional, and midtempo. I like world music, I like african american music in general.
#         Music not liked: I typically don't like rock music, but there are exceptions, typically open-minded artists that are self-conscious of the role of the west in colonalism.
#         Playlist request: It is a nice sunny sunday in december and I would like to listen to some creative and relaxed world music

