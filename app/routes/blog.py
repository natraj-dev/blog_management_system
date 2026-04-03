from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.blog import BlogCreate, BlogResponse, BlogListResponse
from app.services.blog_service import (
    create_blog,
    get_blogs,
    get_blog_by_id,
    update_blog,
    delete_blog
)
from app.core.dependencies import get_db, require_role

router = APIRouter()


#  CREATE BLOG
@router.post("/create", response_model=BlogResponse)
def create_blog_api(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["author"]))
):
    return create_blog(db, blog, current_user.id)


#  GET ALL BLOGS
@router.get("/all", response_model=BlogListResponse)
def get_all_blogs(
    skip: int = 0,
    limit: int = 10,
    search: str = Query(None),
    status: str = Query(None),
    author_id: int = Query(None),
    sort: str = Query(None),
    db: Session = Depends(get_db)
):
    return get_blogs(db, skip, limit, search, status, author_id, sort)


#  GET BLOG BY ID
@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


#  UPDATE BLOG
@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog_api(
    blog_id: int,
    blog: BlogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["author"]))
):
    result = update_blog(db, blog_id, blog, current_user)

    if result is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    if result == "not_allowed":
        raise HTTPException(status_code=403, detail="Not allowed")

    return result


#  DELETE BLOG
@router.delete("/{blog_id}")
def delete_blog_api(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["author", "admin"]))
):
    result = delete_blog(db, blog_id, current_user)

    if result is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    if result == "not_allowed":
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Blog deleted successfully"}
