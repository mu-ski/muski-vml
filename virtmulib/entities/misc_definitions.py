import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

class StrEnum(Enum):
    def __str__(self):
        return f"{self.name}"

class MusicModelAttributeEnum(StrEnum):
    pass

class MusicModel(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)
    pass

class SimpleDate:
    dt: datetime.date

    def __init__(self, dt: str) -> list:
        lis = [int(i) for i in dt.split("-")]
        if len(lis) < 3:
            default_date = [1900, 1, 1]
            lis.extend(default_date[len(lis) :])
        self.dt = datetime.date(*lis)

    def __repr__() -> str:
        return dt.isoformat()

class AIAgentEnum(StrEnum):
    llamma_2_70gb = "llamma_2_70gb"

class ReleaseTypeEnum(StrEnum):
    album = "album"
    single = "single"
    compilation = "compilation"

    @classmethod
    def get_release_enum_by_name(cls, name: str) -> "ReleaseTypeEnum":
        nm = name.lower().strip()
        if nm.find("album") > -1:
            return ReleaseTypeEnum.album
        elif nm.find("single") > -1:
            return ReleaseTypeEnum.single
        elif nm.find("compilation") > -1:
            return ReleaseTypeEnum.compilation
        return None

class AIAgentSetup(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)

    agent: AIAgentEnum
    setup: Optional[str] = None

"""

From: https://stackoverflow.com/questions/76686888/using-bson-objectid-in-pydantic-v2/77105412#77105412

"""

from typing import Any
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)
