import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class UserNode(BaseModel):
    uid: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow().timestamp)

    def __str__(self) -> str:
        return self.uid

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "sanjeethboddi",
            }
        }
    

class UserRelationship(BaseModel):
    uid: str = Field(alias="_id")
    uid2: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow().timestamp)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uid": "sanjeethboddi",
                "uid2": "sanjeethboddi2"
            }
        }


