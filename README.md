![demo](https://github.com/n42r/virtmulib/blob/main/docs/screen-capture.gif?raw=true)

# Muze

Muze is a music discovery and recommendation CLI tool. I built this tool because music discovery has been a personal interest for some time. I uses an LLM as a backend and aske the users several questions about their interests and 

Virtual music library and music recommendation engine

## Architecture

In addition, I also wanted to explore the [Clean / Hexagonal](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) architectural pattern in this project, so I followed that style here although the size of the project is very small to warrant that. Below are the main components in the architecture:

![architecture](https://github.com/n42r/virtmulib/blob/main/docs/arch.drawio.svg?raw=true)

- Domain Model: the core models/data objects which are a list of tracks, collections, users
- Onloader: loads user data (music library, liked, tracks, etc) from external services
- Curator: LLM-powered component to create playlists. I discuss with the user their music taste / interests and generates a playlist
- Offloader: Links items in the intenal Virtual Music Library of the user (typically a newly generated plalyist) to external services where the music can be heard
