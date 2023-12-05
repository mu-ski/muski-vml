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
If the details of a use-case change, then some code in this layer will certainly be affected."

- https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

"""
from pydantic import EmailStr

from virtmulib.entities import *
from virtmulib.applogic.onloader import OnLoader, OnLoaderAuthError

# class LoginSignup:
# 	def __call__(self, onloader: OnLoader) -> EmailStr:
# 		try:
# 			return onloader().login_signup()
# 		except OnLoaderAuthError as e:
# 			print(str(e))

class GetUserData:
	def __call__(self, onloader: type) -> None:
		try:
			return onloader.login_onload_user_data()
		except OnLoaderAuthError as e:
			print(str(e))


class GetUserDataPlaylists:
	def __call__(self, onloader: type) -> list[Playlist]:
		try:
			return onloader.get_playlists()
		except OnLoaderAuthError as e:
			print(str(e))


class GetUserDataAlbums:
	def __call__(self, onloader: type) -> list[Album]:
		try:
			return onloader.get_albums()
		except OnLoaderAuthError as e:
			print(str(e))



class GetUserDataTracks:
	def __call__(self, onloader: type) -> list[Track]:
		try:
			return onloader.get_tracks()
		except OnLoaderAuthError as e:
			print(str(e))

class GetUserDataArtists:
	def __call__(self, onloader: type) -> list[Artist]:
		try:
			return onloader.get_artists()
		except OnLoaderAuthError as e:
			print(str(e))
