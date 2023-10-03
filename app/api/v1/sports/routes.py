from fastapi import APIRouter

sports_router = APIRouter()

@sports_router.get("/")
async def list_sports():
    return {"sports": ["Soccer", "Basketball", "Tennis"]}

@sports_router.get("/{sport_id}")
async def read_sport(sport_id: int):
    return {"sport_id": sport_id}

