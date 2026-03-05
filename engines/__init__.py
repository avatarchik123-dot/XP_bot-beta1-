from .reaction_engine import router as reaction_router
from .level_engine import router as level_router
from .admin_engine import router as admin_router
from .hr_engine import router as hr_router

routers = [
    reaction_router,
    level_router,
    admin_router,
    hr_router
]