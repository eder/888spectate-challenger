from fastapi import FastAPI
from db import db

app = FastAPI()

@app.on_event("startup")
async def startup():

@app.on_event("shutdown")
async def shutdown():
    await db.pop_bind().close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

