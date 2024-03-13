from pydantic import BaseModel
from datetime import datetime
from typing import List

class AuthorBase(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookSchema(BookBase):
    authors: List[AuthorBase]

class AuthorSchema(AuthorBase):
    books: List[BookBase]

class CreateAuthor(BaseModel):
    name: str

    class Config:
        orm_mode: True

class CreateBook(BaseModel):
    title: str
    authors: List[CreateAuthor] 

    class Config:
        orm_mode = True