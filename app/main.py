from fastapi import FastAPI, APIRouter, HTTPException

from db.models import Sport as SportDBModel
from schemas import SportBase, SportResponse, SportCreate



app = FastAPI()

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass
   # await db.pop_bind().close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

