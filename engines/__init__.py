from .xp_engine import router as xp_router
from .reaction_engine import router as reaction_router
from .admin_engine import router as admin_router
from .level_engine import router as level_router

routers = [
    xp_router,
    reaction_router,
    admin_router,
    level_router
]