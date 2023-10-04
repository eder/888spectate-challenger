from fastapi import FastAPI

from api.v1.events.routes import events_router
from db.database import connect_to_db, close_db_connection

app = FastAPI()

app.include_router(events_router, prefix="/api/v1/events", tags=["events"])


@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()

