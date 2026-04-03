from sqlalchemy.orm import Session
from app.models.comment import Comment


def create_comment(db: Session, content: str, blog_id: int, user_id: int):
    comment = Comment(
        content=content,
        blog_id=blog_id,
        user_id=user_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def get_comments_by_blog(db: Session, blog_id: int):
    return db.query(Comment).filter(Comment.blog_id == blog_id).all()


def delete_comment(db: Session, comment_id: int, user):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        return None

    if comment.user_id != user.id and user.role != "admin":
        return "not_allowed"

    db.delete(comment)
    db.commit()

    return comment
