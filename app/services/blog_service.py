from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.blog import Blog
from app.schemas.blog import BlogCreate
from app.services.audit_service import create_audit_log


# CREATE BLOG
def create_blog(db: Session, blog: BlogCreate, user_id: int):
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        status=blog.status,
        author_id=user_id
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    create_audit_log(db, user_id, f"Created blog {new_blog.id}")

    return new_blog


#  GET BLOGS WITH SEARCH + FILTER + SORT + PAGINATION
def get_blogs(
    db: Session,
    skip=0,
    limit=10,
    search=None,
    status=None,
    author_id=None,
    sort=None
):
    query = db.query(Blog)

    if search:
        query = query.filter(
            or_(
                Blog.title.ilike(f"%{search}%"),
                Blog.content.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(Blog.status == status)

    if author_id:
        query = query.filter(Blog.author_id == author_id)

    if sort == "created_at":
        query = query.order_by(Blog.created_at.desc())

    elif sort == "title":
        query = query.order_by(Blog.title.asc())

    total = query.count()
    blogs = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "blogs": blogs
    }


#  GET SINGLE BLOG
def get_blog_by_id(db: Session, blog_id: int):
    return db.query(Blog).filter(Blog.id == blog_id).first()


#  UPDATE BLOG
def update_blog(db: Session, blog_id: int, blog_data: BlogCreate, user):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        return None

    if blog.author_id != user.id:
        return "not_allowed"

    blog.title = blog_data.title
    blog.content = blog_data.content
    blog.status = blog_data.status

    db.commit()
    db.refresh(blog)

    create_audit_log(db, user.id, f"Updated blog {blog_id}")

    return blog


# DELETE BLOG
def delete_blog(db: Session, blog_id: int, user):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        return None

    if blog.author_id != user.id and user.role != "admin":
        return "not_allowed"

    db.delete(blog)
    db.commit()

    create_audit_log(db, user.id, f"Deleted blog {blog_id}")

    return blog
