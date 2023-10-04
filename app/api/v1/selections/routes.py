from fastapi import APIRouter, Depends

from utils.dependencies import get_selection_service
from schemas import SelectionBase
from services.selection_service import SelectionService
from repositories.selection_repository import SelectionRepository 

selections_router = APIRouter()

@selections_router.get("/selections/")
async def get_all_selections(service: SelectionService = Depends(get_selection_service)):
    return await service.get_all()


@selections_router.post("/selections/")
async def create_selection(selection: SelectionBase, service: SelectionService = Depends(get_selection_service)):
    return await service.create(selection.dict())

