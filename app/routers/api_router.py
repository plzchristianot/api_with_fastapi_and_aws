from fastapi import APIRouter, HTTPException, status
from app.routers import users

router = APIRouter()

router.include_router(users.router, 
                      prefix="/users", 
                      tags=["users"], 
                      responses={status.HTTP_201_CREATED:{"message":"The user has been created"}})
