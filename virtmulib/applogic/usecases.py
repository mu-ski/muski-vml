"""
Use Cases: Business Rules of the application

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
from abc import ABC
from attrs import define

from virtmulib.entities import Playlist, Album, Track, Library, Artist, VMLThing
from virtmulib.applogic.onloader import OnLoad, OnLoaderAuthError

@define
class OnloaderAction(ABC):
    OnLoad: type
    f_name: str

    def execute(self) -> VMLThing:
        try:
            func = getattr(self.OnLoad, self.f_name)
            return func()
        except OnLoaderAuthError as e:
            print(str(e))
            return None

@define
class GetUserData(OnloaderAction):
    f_name: str = "login_onload_user_data"

@define
class GetUserDataPlaylists(OnloaderAction):
    f_name: str = "get_playlists"

@define
class GetUserDataAlbums(OnloaderAction):
    f_name: str = "get_albums"

@define
class GetUserDataTracks(OnloaderAction):
    f_name: str = "get_tracks"

@define
class GetUserDataArtists(OnloaderAction):
    f_name: str = "get_artists"


# class LoginSignup:
#     def __call__(self, OnLoad: OnLoad) -> EmailStr:
#         try:
#             return OnLoad().login_signup()
#         except OnLoaderAuthError as e:
#             print(str(e))
