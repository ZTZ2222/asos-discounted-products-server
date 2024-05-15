from time import time
from jose import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings
from src.models.user import User


async def get_from_redis(request: Request, key: str):
    return await request.app.state.redis.get(key)


async def set_to_redis(request: Request, key: str, value: str, ex: int):
    return await request.app.state.redis.set(key, value, ex=ex)


async def verify_jwt(request: Request, token: str) -> bool:
    payload = await get_from_redis(request, token)
    return bool(payload)


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )
        if not await verify_jwt(request, credentials.credentials):
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        return credentials.credentials


async def create_access_token(user: User, request: Request):
    payload = {
        "email": user.email,
        "expiry": time.time() + settings.JWT_EXPIRE,
        "platform": request.headers.get("User-Agent"),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    _bool = await set_to_redis(request, token, str(payload), ex=settings.JWT_EXPIRE)
    if _bool:
        return token
