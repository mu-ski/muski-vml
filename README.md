# Muski VML (Virtual Music Library)

The *virtual music library* and *music recommendation engine* powering muski


# Product Overview

Personalized playlist creator and recommender. 

**Uses:** 
1. spotify user data
2. user responses to questions about their taste
3. user input about the theme/subject of a desired playlist (or the service recommeds one)

**To:**
Curate and a playlists for them and add it to their spotify account


## MVP

1. REST API only
2. User logs in using their spotify
3. Spotify user data is retrieved from account
4. A cutomized chat session with an LLM where the user is asked question to understand their relationship / tastes in music
5. A subject/theme of a playlist is identified (or recommeded by the service)
6. A playlist is created on the user spotify account

## Architecture

This project will use the [Clean / Hexagonal](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) architectural pattern in the sense of having one-way dependancies from the outside components to the core/model component, and using adapters and ports to exchange data across layers.

Below are the main components:
```
	Onloader
	   |
	   |
     Domain Model  ---- Curator 
	   |
	   |
	Offloader
```

- Domain Model: the core models/data objects which are a list of tracks, collections, users
- Onloader: loads user data (music library, liked, tracks, etc) from external services
- Curator: LLM-powered component to create playlists. I discuss with the user their music taste / interests and generates a playlist
- Offloader: Links items in the intenal Virtual Music Library of the user (typically a newly generated plalyist) to external services where the music can be heard


## Folder Structure

- 
