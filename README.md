# Muze (Back-end)

Muze is an AI/LLM-driven music discovery and recommendation service.

![demo](https://github.com/n42r/virtmulib/blob/main/docs/screen-capture.gif?raw=true)

This is part of a larger web-based / mobile service that I was planning on, it contains the core functionality accessible from the CLI. I built it to test the limit of LLM/AI-driven music recommendation and explore whether I want to dive deeper in this direction. 

I ended up deciding to follow a different route in music recommendation and discovery (human/social-driven). It was also an opportunity for me to explore the Clean / Hexagonal / modular monolith architecture (see below). I also wanted to experiment with recently revamped python tools such as Pydantic 2 and so on.

Overall, I think this project might be interesting to anyone who wants to build an AI-driven music recommendation. I am not hosting it anymore due to LLM hosting costs being too high for an aborted project.

## Architecture

I wanted to explore the [Clean / Hexagonal](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) architectural pattern in this project, so I followed that style here although the size of the project is very small to warrant that. Below are the main components in the architecture:

![architecture](https://github.com/n42r/virtmulib/blob/main/docs/arch.drawio.svg?raw=true)

- Domain Model: the core models/data objects which are a list of tracks, collections, users
- Onloader: loads user data (music library, liked, tracks, etc) from external services
- Curator: LLM-powered component to create playlists. I discuss with the user their music taste / interests and generates a playlist
- Offloader: Links items in the intenal Virtual Music Library of the user (typically a newly generated plalyist) to external services where the music can be heard
