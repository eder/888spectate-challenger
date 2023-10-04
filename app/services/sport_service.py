from repositories.sport_repository import SportRepository

class SportService:

    def __init__(self, repository: SportRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, sport):
        return await self.repository.create(sport)

