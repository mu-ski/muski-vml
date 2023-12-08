from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict
from bson import ObjectId
from pydantic_core import core_schema


class MusicModelAttributeEnum(str, Enum):
    pass


class MusicModel(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)


class AIAgentEnum(str, Enum):
    llamma_2_70gb = "llamma_2_70gb"


class ReleaseTypeEnum(str, Enum):
    ALBUM = "ALBUM"
    SINGLE = "SINGLE"
    COMPILATION = "COMPILATION"

    @classmethod
    def get_enum(cls, name: str) -> "ReleaseTypeEnum":
        nm = name.lower().strip()
        if nm.find("album") > -1:
            return ReleaseTypeEnum.ALBUM
        if nm.find("single") > -1:
            return ReleaseTypeEnum.SINGLE
        if nm.find("compilation") > -1:
            return ReleaseTypeEnum.COMPILATION
        return None


class AIAgentSetup(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)

    agent: AIAgentEnum
    setup: Optional[str] = None


class PyObjectId(str):
    """
    From: https://stackoverflow.com/questions/76686888/using-bson-objectid-in-pydantic-v2/77105412#77105412

    """

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
