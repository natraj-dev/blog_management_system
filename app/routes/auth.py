from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.auth_service import create_user, login_user
from app.core.dependencies import get_db
from app.core.security import create_access_token
from app.config import SECRET_KEY, ALGORITHM

from app.services.audit_service import create_audit_log

router = APIRouter()


#  REGISTER
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


#  LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, user.email, user.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = result["access_token"]

    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")

    if user_id:
        create_audit_log(db, int(user_id), "User logged in")

    return result


#  REQUEST SCHEMA
class RefreshTokenRequest(BaseModel):
    refresh_token: str


#  REFRESH TOKEN
@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    new_access_token = create_access_token({
        "sub": user_id,
        "role": payload.get("role")
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
