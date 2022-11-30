from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from neo4j.exceptions import ConstraintError

from models import UserNode, UserRelationship

router = APIRouter()

@router.post("/createUser/", response_description="Create a new user")
async def create_profile(request: Request, userNode: UserNode = Body(...)):
    try:
        result =  request.app.neo4j_client.create_user(userNode)
    except ConstraintError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return

@router.delete("/deleteUser/", response_description="Delete a user")
async def delete_profile(request: Request, userNode: UserNode = Body(...)):
    request.app.neo4j_client.delete_user(userNode)
    return
    
@router.put("/followUser/", response_description="Follow a user")
async def follow_user(request: Request, userRelationship: UserRelationship = Body(...)):
    try:
        result =  request.app.neo4j_client.follow_user(userRelationship)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User1 already follows User2")
    return


@router.put("/unfollowUser/", response_description="Unfollow a user")
async def unfollow_user(request: Request, userRelationship: UserRelationship = Body(...)):
    request.app.neo4j_client.unfollow_user(userRelationship)
    return

@router.get("/getFollowersList/{user_id}", response_description="Get followers of a user", response_model=List[str])
async def get_followers_list(request: Request, user_id: str):
    return request.app.neo4j_client.get_followers_list(user_id)
    
     


@router.get("/getFollowingList/{user_id}", response_description="Get following of a user", response_model=List[str])
async def get_following_list(request: Request, user_id: str):
    return request.app.neo4j_client.get_following_list(user_id)

@router.get("/getFollowingCount/{user_id}", response_description="Get following of a user", response_model=int)
async def get_following_count(request: Request, user_id: str):
    return request.app.neo4j_client.get_following_count(user_id)

@router.get("/getFollowerCount/{user_id}", response_description="Get follower count of a user", response_model=int)
async def get_follower_count(request: Request, user_id: str):
    return request.app.neo4j_client.get_follower_count(user_id)

@router.get("/getFollowSuggestions/{user_id}", response_description="Get follow suggestions for a user", response_model=List[str])
async def get_follow_suggestions(request: Request, user_id: str):
    return request.app.neo4j_client.get_follow_suggestions(user_id)