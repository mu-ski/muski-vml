# Muze

Muze is a music discovery and recommendation tool. 

![demo](https://github.com/n42r/virtmulib/blob/main/docs/screen-capture.gif?raw=true)

It was a prototype to test the limit of LLM/AI-driven music recommendation and explore whether I want to dive deeper in that direction in a more serious direction. I ended up deciding to follow a different direction in music recommendation and discovery. It was also an opportunity for me to explore the Clean / Hexagonal modular monolith architectural pattern (see below). I also wanted to experiment with recent python tools such as Pydantic.

Overall, I think this project might be interesting to those who want to build AI-driven music recommendation. Sadly, I am not hosting it anymore due to LLM hosting costs being too high for an aborted project.

## Architecture

In addition, I also wanted to explore the [Clean / Hexagonal](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) architectural pattern in this project, so I followed that style here although the size of the project is very small to warrant that. Below are the main components in the architecture:

![architecture](https://github.com/n42r/virtmulib/blob/main/docs/arch.drawio.svg?raw=true)

- Domain Model: the core models/data objects which are a list of tracks, collections, users
- Onloader: loads user data (music library, liked, tracks, etc) from external services
- Curator: LLM-powered component to create playlists. I discuss with the user their music taste / interests and generates a playlist
- Offloader: Links items in the intenal Virtual Music Library of the user (typically a newly generated plalyist) to external services where the music can be heard
