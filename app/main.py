from fastapi import FastAPI
from api.v1.sports.routes import sports_router

app = FastAPI()

app.include_router(sports_router, prefix="/sports", tags=["sports"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}

