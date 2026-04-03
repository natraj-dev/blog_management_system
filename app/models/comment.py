from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from app.database import Base

# create comment table


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
