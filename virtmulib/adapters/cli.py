def printn(s, empty_return=True, inpt=True):
    note2 = "Press enter ⏎..." if empty_return else ">> "
    print(s)
    _printn()
    if inpt:
        inp = input(note2)
        _printn()
        return inp
    return None


def _printn(n=15, s=""):
    for i in range(0, n):
        print(s)


def emit(str):
    return printn(str, inpt=False)


def greet():
    printn(" >> Welcome! I'm 🎶Muze🎶, an app to help you enjoy music again!")
    printn(" >> Muze is a tool to help you find music you enjoy.")
    printn(
        " >> It does that by asking you for your preferences and creating a custom-made playlist for you automatically on your spotify account."
    )
    printn(" >> Muze works as follows:")
    printn(
        " >> 1. First, you give the Muze access to your spotify: it uses your spotify data to create a new Muze account and understands what music you like."
    )
    printn(
        " >> 2. Second, you answer a couple of questions about your music preferences (only on the first time you register)."
    )
    printn(
        " >> 3. Finally, the good part, you describe what kind of music you want to hear right NOW, and, voilà!, you will have a new playlist on your spotify."
    )
    printn(
        " >> Ready to start? 😀 As soon as you press enter ⏎, your browser will open the spotify website, and you will be asked to allow Muze to read your data."
    )
    # printn(" >> As soon as you press enter ⏎, your browser will open the spotify website, and you will be asked to allow Muze to read your data.", inpt=False)
    # input()


def query_user():
    printn(" >> Great! Step 1 of 3 done ✔️. Now for the juicy part, the questions.")
    ans1 = printn(
        " >> First: Tell us below 👇 what does music mean to you? And when do you typically listen to music? (Take your time and get creative, the more detail, the better 😉)",
        empty_return=False,
    )
    ans2 = printn(
        " >> Second: What music do you typically avoid / dislike?", empty_return=False
    )
    printn(
        " >> Thank you! Step 2 of 3 done ✔️ (We'll store your answers so you don't have to enter them next time."
    )
    # ans3 = printn(" >> Third: What kinds of music do you dislike?", empty_return=False)
    return ans1, ans2


def query_user_playlist():
    ans3 = printn(
        " >> What's your mood like right NOW, what music do you feel like listening to? (Ex., 'sunny saturday morning music from Mali',  '70s disco music')",
        empty_return=False,
    )
    if not ans3:
        ans3 = printn(
            " >> You need to tell us what music you want to listen to. More examples: 'Saxophone-led rock music',  '90s dance pop'",
            empty_return=False,
        )
    printn(" >> Done! ✔️✔️✔️ You did your part, now it's our turn!")
    emit(
        "Discovering the best music for you 🤩🎵🎶... Hold on tight, this might take a minute..."
    )
    return ans3


# def query_returning_user():
#     ans4 = printn(" >> What's your mood like now, what music do you want to listen to THIS moment? (Ex., 'sunny saturday morning music from Mali',  '70s disco music')", empty_return=False)
#     if not ans4:
#         ans4 = printn(" >> You need to tell us what music you want to listen to. More examples: 'Saxophone-led rock music',  '90s dance pop'", empty_return=False)
#     printn(" >> Done! ✔️✔️✔️ You did your part, not it's our turn!")
#     emit("Discovering the best music for you 🤩🎵🎶... Hold on tight, this might take a minute...")
#     return ans4


#         Top songs: Herbie Hancock - Maiden Voyage, Laika - Praire Dog
#         What music means to me: Music is what I listen to when I need to discover new feelings and new imagination
#         Liked Music: I like many kinds of music, as long as its creative, emotional, and midtempo. I like world music, I like african american music in general.
#         Music not liked: I typically don't like rock music, but there are exceptions, typically open-minded artists that are self-conscious of the role of the west in colonalism.
#         Playlist request: It is a nice sunny sunday in december and I would like to listen to some creative and relaxed world music
