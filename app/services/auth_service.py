from app.models.audit import AuditLog
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, create_refresh_token


def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pwd,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        return None

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def create_audit_log(db: Session, user_id: int, action: str):
    log = AuditLog(
        user_id=user_id,
        action=action
    )

    db.add(log)
    db.commit()
