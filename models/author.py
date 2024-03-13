from database import Base, get_db
from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, select
from sqlalchemy.ext.declarative import declarative_base

class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer,primary_key=True,nullable=False)
	name = Column(String,nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
	updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))