from fastapi import APIRouter, Depends, HTTPException

from schemas import SelectionBase, SelectionUpdate, SearchNameModel
from services.selection_service import SelectionService
from repositories.selection_repository import SelectionRepository
from utils.custom_exceptions import CreationError, ValidationError, ForeignKeyError
from utils.dependencies import get_selection_service


selections_router = APIRouter()


@selections_router.get("/selections/")
async def get_all_selections(
    service: SelectionService = Depends(get_selection_service),
):
    return await service.get_all()


@selections_router.post("/selections/")
async def create_selection(
    selection: SelectionBase, service: SelectionService = Depends(get_selection_service)
):
    try:
        return await service.create(selection.dict())

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except CreationError as ce:
        raise HTTPException(status_code=400, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@selections_router.put("/selections/{selection_id}")
async def update_selection(
    selection_id: int,
    selection: SelectionUpdate,
    service: SelectionService = Depends(get_selection_service),
):
    
    try:
        updated_selection = await service.update(selection_id, selection.dict())
    except ForeignKeyError:
        raise HTTPException(status_code=400, detail="Invalid event ID provided.")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    if not updated_selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    return updated_selection


@selections_router.post("/selections/search/")
async def search_sports(
    criteria: SearchNameModel,
    service: SelectionService = Depends(get_selection_service),
):
    return await service.search_selections(criteria)
