"""
Use Cases: Business Rules of the application

This module contains an interface to the holistic behaviours of the system.
These actions are what is tested in unit testing, each use-case is a unit. 
This module is a kind of abstraction/interface and gateway layer 
with no new logic and just calls to the respective underlying functionality.

This is probably the best place to start reading the code.

This module is part of the application logic layer in the clean architecture:

"The software in this layer contains application specific business rules.
It encapsulates and implements all of the use cases of the system.
These use cases orchestrate the flow of data to and from the entities,
and direct those entities to use their enterprise wide business rules
to achieve the goals of the use case.

We do not expect changes in this layer to affect the entities.
We also do not expect this layer to be affected by changes to externalities
such as the database, the UI, or any of the common frameworks.
This layer is isolated from such concerns.

We do, however, expect that changes to the operation of the application
will affect the use-cases and therefore the software in this layer.
If the details of a use-case change, then some code in this layer 
will certainly be affected."
- https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

"""

import virtmulib.applogic.onload.gateway as onload_gateway
from virtmulib.applogic.onload.abstract import OnLoad


def login_singup_user(onload_type: OnLoad):
    return onload_gateway.UserLogin(onload_type).execute()


def get_user_data(onload_type: OnLoad):
    return onload_gateway.GetUserData(onload_type).execute()


def get_user_playlists(onload_type: OnLoad):
    return onload_gateway.GetUserDataPlaylists(onload_type).execute()


def get_user_albums(onload_type: OnLoad):
    return onload_gateway.GetUserDataAlbums(onload_type).execute()


def get_user_artists(onload_type: OnLoad):
    return onload_gateway.GetUserDataArtists(onload_type).execute()


def get_user_tracks(onload_type: OnLoad):
    return onload_gateway.GetUserDataTracks(onload_type).execute()
