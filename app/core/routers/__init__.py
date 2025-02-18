from core.routers.items import router as items_router
from utils.api.router import TypedAPIRouter

items_router = TypedAPIRouter(router=items_router, prefix="/items", tags=["item"])
