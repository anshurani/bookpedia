from database import Base, get_db
from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class BookAuthor(Base):
	__tablename__ = "book_authors"

	id = Column(Integer,primary_key=True,nullable=False)
	book_id = Column(ForeignKey('books.id'), primary_key=True)
	author_id = Column(ForeignKey('authors.id'), primary_key=True)
	blurb = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
	updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))