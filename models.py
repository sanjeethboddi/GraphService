import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# - [GET]/getDisplayName(userId) —> String displayName
# - [GET]/getDateOfBirth(userId) —> Date dateOfBirth
# - [GET]/getAddress(userId) —> Location address
# - [GET]/getFollowersCount(userId) —> Long followersCount
# - [GET]/getFollowingCount(userId) —> Long followingCount
# - [GET]/getPetsList(userId) —> List<PetIds> petsList
# - [PUT]/setDisplayName(userId, displayName) —> None
# - [PUT]/setDateOfBirth(userId, dateOfBirth) —> None
# - [PUT]/setAddress(userId, address) —> None
# - [POST]/createProfile(userId, displayName, dateOfBirth, address) —> None

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


# u1 = UserNode(uid="sanjeethbodi")
# u2 = UserNode(uid="sanjee")
# r1 = UserRelationship(uid=u1, uid2=u2)
# print(u1.get_create_node_query())
# print(r1.get_create_relationship_query())
