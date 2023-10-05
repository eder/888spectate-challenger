from repositories.sport_repository import SportRepository

class SportService:

    def __init__(self, sport_repository: SportRepository):
        self.sport_repository = sport_repository

    async def get_all(self):
        return await self.sport_repository.get_all()

    async def create(self, sport):
        return await self.sport_repository.create(sport)
    
    async def update(self, sport_id: int, sport_data: dict) -> dict:
        return await self.sport_repository.update(sport_id, sport_data)

