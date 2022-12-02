from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from neo4j.exceptions import ConstraintError

from models import UserNode, UserRelationship
import requests

router = APIRouter()

@router.post("/createUser/{token}", response_description="Create a new user")
def create_profile(token:str, request: Request, userNode: UserNode = Body(...)):
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if  resp.status_code != 200 or resp.json()["username"] != userNode.uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result =  request.app.neo4j_client.create_user(userNode)
    except ConstraintError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return

@router.delete("/deleteUser/{token}", response_description="Delete a user")
def delete_profile(token:str, request: Request, userNode: UserNode = Body(...)):
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if  resp.status_code != 200 or resp.json()["username"] != userNode.uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    request.app.neo4j_client.delete_user(userNode)
    return
    
@router.put("/followUser/{token}", response_description="Follow a user")
def follow_user(token:str, request: Request, userRelationship: UserRelationship = Body(...)):
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if  resp.status_code != 200 or resp.json()["username"] != userRelationship.uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result =  request.app.neo4j_client.follow_user(userRelationship)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User1 already follows User2")
    return


@router.put("/unfollowUser/{token}", response_description="Unfollow a user")
def unfollow_user(token:str, request: Request, userRelationship: UserRelationship = Body(...)):
    resp =  requests.post(request.app.auth_service+f"/verify/{token}")
    if  resp.status_code != 200 or resp.json()["username"] != userRelationship.uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    request.app.neo4j_client.unfollow_user(userRelationship)
    return

@router.get("/getFollowersList/{user_id}", response_description="Get followers of a user", response_model=List[str])
def get_followers_list(request: Request, user_id: str):
    return request.app.neo4j_client.get_followers_list(user_id)
    

@router.get("/getFollowingList/{user_id}", response_description="Get following of a user", response_model=List[str])
def get_following_list(request: Request, user_id: str):
    return request.app.neo4j_client.get_following_list(user_id)

@router.get("/getFollowingCount/{user_id}", response_description="Get following of a user", response_model=int)
def get_following_count(request: Request, user_id: str):
    return request.app.neo4j_client.get_following_count(user_id)

@router.get("/getFollowerCount/{user_id}", response_description="Get follower count of a user", response_model=int)
def get_follower_count(request: Request, user_id: str):
    return request.app.neo4j_client.get_follower_count(user_id)

@router.get("/getFollowSuggestions/{user_id}", response_description="Get follow suggestions for a user", response_model=List[str])
def get_follow_suggestions(request: Request, user_id: str):
    return request.app.neo4j_client.get_follow_suggestions(user_id)