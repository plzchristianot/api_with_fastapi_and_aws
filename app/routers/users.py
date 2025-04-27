from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from app.schemas.users import UpdateUser, Users, UserBase
from app.controllers.users import clean_up
# from app.db.users import db
import boto3
from app.responses.users import SuccessResponse, ErrorResponse
import logging
import pandas as pd
import json
import psycopg2

#from pyjwt import pyjwt

router = APIRouter()
oauth2_scheme = HTTPBearer()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

conn = psycopg2.connect(
            host='example.c3mqa60k2ubs.us-west-1.rds.amazonaws.com',
            database='postgres',
            user='postgres',
            password='ultimatez',
            port=5432
        )

db = conn.cursor()

@router.post("/create", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: Users,
    token: HTTPBearer = Depends(oauth2_scheme)
):
    try:
        info = table.get_item(Key={'username': user.username, 'last_name':user.last_name})

    except:
        raise HTTPException(status_code=500, detail="Something went wrong while connecting to DynamoDB")

    if 'Item' in info:
        raise HTTPException(status_code=409, detail={
            "status code" : 409,
            "error" : "The user is already registered"
        })
    
    table.put_item(
        Item= user.dict(),
        ConditionExpression='attribute_not_exists(username)'
        )    

    return SuccessResponse(status_code=201, detail=f"The user {user.username} has been created", data=user.model_dump())

@router.post("/users/bulk")
async def upload_users(users: list[Users]):
    try:
        with table.batch_writer() as batch:
            for user in users:
                batch.put_item(Item=user.model_dump())
                logging.info(f"User added: {user.username}")
                
        return {"message": f"{len(users)} users inserted successfully into DynamoDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/trigger_cleanup")
async def trigger_cleanup():
    try:
        await clean_up()
    except:
        raise ErrorResponse.bad_request
    
    return SuccessResponse(status_code=200, 
                           detail="The cleanup activity has been performed successfully", 
                            )

@router.delete("/delete", response_model= SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user:UserBase
) -> dict:
    
    try:
        info = table.get_item(Key={'username': user.username, 'last_name':user.last_name})
    except:
        raise ErrorResponse.server_error
    
    if 'Item' not in info:
        raise ErrorResponse.not_found
    
    table.delete_item(
        Key={
            'username': user.username,
            'last_name': user.last_name,
        })
    
    return SuccessResponse(status_code=200, 
                           detail=f"The user {user.username} has been removed succesfully", 
                           data=user.model_dump())
    
@router.put("/update", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user: UserBase,
    new_data: UpdateUser
):
    try:
        info = table.get_item(Key={'username': user.username, 'last_name':user.last_name})
        
    except:
        raise ErrorResponse.server_error
    
    if 'Item' not in info:
            raise ErrorResponse.not_found

    unpacked = new_data.model_dump()
    for i in list(unpacked):
        if unpacked[i] == "string":
            unpacked.pop(i)
    items = unpacked.keys()
    for i in items:
        table.update_item(
        Key={
            'username': user.username,
            'last_name': user.last_name
        },
        UpdateExpression=f'SET {i} = :val1',
        ExpressionAttributeValues={
            ':val1':unpacked[i]
        }
    )
        
    return SuccessResponse(status_code=200, detail="The information has been updated", data=new_data.model_dump())

@router.get("/get_users_by_id", response_model=SuccessResponse, status_code=200)
async def get_users_by_id(
    user: UserBase = Depends(UserBase)): 
    try:
        info =  table.get_item(Key={'username': user.username, 'last_name':user.last_name})

    except:
        raise ErrorResponse.server_error
    
    if 'Item' not in info:
            raise ErrorResponse.not_found

    user_info = table.get_item(
        Key={
            'username': user.username,
            'last_name': user.last_name
        }
    )    
    
    return SuccessResponse(status_code=200, detail="The user has been found", data=user_info['Item'])

