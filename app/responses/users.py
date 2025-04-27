from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException, status

class SuccessResponse(BaseModel):
    status_code : Optional[int] = Field(default=200)
    detail : Optional[str] = Field(default="Success")
    data : Optional[dict] = Field(default=None)

class ErrorResponse():
    server_error  = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "status code" : 500,
            "detail" : "Something went wrong while connecting to the database"
        })
    not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "status code" : 404,
                "error" : "The user was not found"
            })
    bad_request = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "status code" : 400,
            "detail" : "The data is already registered in the database"
    })


