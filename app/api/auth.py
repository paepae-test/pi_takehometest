from fastapi import APIRouter, HTTPException, status

import app.schemas.security as security_schemas
from app.core.security import authenticate_app_user_async, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/", response_model=security_schemas.AuthToken)
async def authenticate(auth_data: security_schemas.Auth):
    app_user = await authenticate_app_user_async(username=auth_data.username, password=auth_data.password)

    if not app_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": str(app_user.id)})
    return security_schemas.AuthToken(
        access_token=access_token,
        token_type="bearer",
    )
