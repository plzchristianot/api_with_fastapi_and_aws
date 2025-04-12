from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from app.schemas.users import UpdateUser, Users, UserBase
import boto3
from app.responses.users import SuccessResponse, ErrorResponse
#from pyjwt import pyjwt


router = APIRouter()
oauth2_scheme = HTTPBearer()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

@router.post("/create", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: Users
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
        Item= user.dict()
        )    

    return SuccessResponse(status_code=201, detail=f"The user {user.username} has been created", data=user.model_dump())
    

@router.delete("/delete", response_model= SuccessResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user:UserBase
) -> dict:
    
    try:
        info = table.get_item(Key={'username': user.username, 'last_name':user.last_name})
    except:
        raise HTTPException(status_code=500, detail={
            "status code" : 500,
            "error" : "Something went wrong while connecting to DynamoDB"
        })
    
    if 'Item' not in info:
        raise HTTPException(status_code=404, detail={
            "status code" : 404,
            "error" : "The user was not found"
        })
    
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
