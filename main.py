from fastapi import FastAPI, APIRouter
from app.routers.api_router import router
from mangum import Mangum

app = FastAPI(title="AWS project",
              root_path="/dev"
              
)

app.include_router(router)

@app.get("/")
async def root():
    return "hey!"


handler = Mangum(app)