from fastapi import APIRouter

# from app.endpoints.channels import router as channels_router
from app.endpoints.posts import router as posts_router
from app.endpoints.health import router as health_router
# from app.endpoints.metrics import router as metrics_router
# from app.endpoints.comparing import router as comparing_router
# from app.endpoints.dashboard import router as dashboard_router
# from app.endpoints.prediction import router as prediction_router


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

# router.include_router(channels_router)
router.include_router(health_router)
router.include_router(posts_router)
# router.include_router(metrics_router)
# router.include_router(comparing_router)
# router.include_router(dashboard_router)
# router.include_router(prediction_router)
