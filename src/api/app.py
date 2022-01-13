import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi import Depends, FastAPI

from api.router.user import current_active_user, fastapi_users, jwt_authentication
from config import settings
from database.models import UserDB


def get_application():
    sentry_sdk.init(dsn=settings.sentry_url, traces_sample_rate=1.0)

    app = FastAPI(title="Auth Service")

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(), prefix="/users", tags=["users"]
    )

    @app.get("/authenticated-route")
    async def authenticated_route(user: UserDB = Depends(current_active_user)):
        return {"message": f"Hello {user.email}!"}

    return SentryAsgiMiddleware(app)
