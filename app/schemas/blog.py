from pydantic import BaseModel
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    content: str
    status: str


class BlogResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    status: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class BlogListResponse(BaseModel):
    total: int
    blogs: list[BlogResponse]
