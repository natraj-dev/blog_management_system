from app.core.dependencies import require_role
from app.core.dependencies import get_current_user
from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.models import user
from app.routes import auth
from app.core.dependencies import get_db
from app.models import blog
from app.routes import blog
from app.routes import comment
from app.models import audit
from app.routes import audit

app = FastAPI()

# title's  swagger ui
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(blog.router, prefix="/blog", tags=["Blog"])

app.include_router(comment.router, prefix="/comment", tags=["Comments"])

app.include_router(audit.router, prefix="/audit", tags=["Audit"])
# create tables
Base.metadata.create_all(bind=engine)

# Welcome msg


@app.get("/")
def root():
    return {"message": "Blog API Running"}

# Get current user


@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


# Admin only


@app.get("/admin-only")
def admin_route(user=Depends(require_role(["admin"]))):
    return {"message": "Welcome Admin"}

# Author only


@app.get("/author-only")
def author_route(user=Depends(require_role(["author"]))):
    return {"message": "Welcome Author"}


# User only


@app.get("/user-only")
def user_route(user=Depends(require_role(["user"]))):
    return {"message": "Welcome User"}
