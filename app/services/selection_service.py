from repositories.selection_repository import SelectionRepository 

class SelectionService:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, selection):
        return await self.repository.create(selection)
