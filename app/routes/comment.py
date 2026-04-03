from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate
from app.services.comment_service import (
    create_comment,
    get_comments_by_blog,
    delete_comment
)
from app.core.dependencies import get_db, require_role

# create router
router = APIRouter()

# create cmt


@router.post("/create")
def create_comment_api(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["user", "author", "admin"]))
):
    return create_comment(
        db,
        comment.content,
        comment.blog_id,
        current_user.id
    )

# get cmt


@router.get("/blog/{blog_id}")
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    return get_comments_by_blog(db, blog_id)

# delete cmt


@router.delete("/{comment_id}")
def delete_comment_api(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["user", "author", "admin"]))
):
    result = delete_comment(db, comment_id, current_user)

    if result is None:
        return {"detail": "Comment not found"}

    if result == "not_allowed":
        return {"detail": "Not allowed"}

    return {"message": "Comment deleted"}
