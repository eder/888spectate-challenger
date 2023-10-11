from fastapi import FastAPI

from db.database import connect_to_db, close_db_connection

from api.v1.events.routes import events_router
from api.v1.sports.routes import sports_router
from api.v1.selections.routes import selections_router


app = FastAPI()

app.include_router(sports_router, prefix="/api/v1", tags=["sports"])
app.include_router(events_router, prefix="/api/v1", tags=["events"])
app.include_router(selections_router, prefix="/api/v1", tags=["selections"])


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()
