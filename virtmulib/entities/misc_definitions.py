import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SimpleDate:
	dt: datetime.date
	def __init__(self, dt: str) -> list:
		lis = [int(i) for i in dt.split('-')]
		if len(lis) < 3:
			default_date = [1900, 1, 1]
			lis.extend(default_date[len(lis):])
		self.dt=datetime.date(*lis) 

class AIAgentEnum(Enum):
	llamma_2_70gb = 'llamma_2_70gb'

class ReleaseTypeEnum(Enum):
	album = 'album'
	single = 'single'
	compilation = 'compilation'

class MusicModel(BaseModel):
	model_config = ConfigDict(extra='allow',validate_assignment=True)
	
	pass

class AIAgentSetup(BaseModel):
	model_config = ConfigDict(extra='allow',validate_assignment=True)
	
	agent: AIAgentEnum
	setup: Optional[str] = None
