from fastapi import APIRouter

from app.api.v1.routes import auth_routes, user_routes, task_routes


api_router = APIRouter()

api_router.include_router(auth_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(task_routes.router)