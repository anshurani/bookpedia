from database import Base, get_db
from typing import Annotated, Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, select, insert, func, update
from sqlalchemy.ext.declarative import declarative_base
from .author import Author
from .book_author import BookAuthor

class Book(Base):
	__tablename__ = "books"

	id = Column(Integer,primary_key=True,nullable=False)
	title = Column(String,nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
	updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class BookRepository:
	def __init__(self, db: Annotated[Session, Depends(get_db)]):
		self.db = db

	def get_books(self, id: Optional[int] = None):
		authors_agg = func.array_agg(func.jsonb_build_object('id', Author.id, 'name', Author.name, 'created_at', Author.created_at, 'updated_at', Author.updated_at)).label('authors')

		stmt = select(Book, authors_agg)\
				.join(BookAuthor, BookAuthor.book_id == Book.id)\
				.join(Author, BookAuthor.author_id == Author.id)\
				.filter(*([Book.id == id] if id else []))\
				.group_by(Book.id)

		result = self.db.execute(stmt).all()
		return result

	def create_book(self, request_params):
		with self.db as session:
			session.begin()
			try:
				book_author_params = []
				book = session.scalars(
					insert(Book)
					.values([{'title' : request_params["title"]}])
					.returning(Book)
				).all()

				authors = session.scalars(
					insert(Author)
					.values(request_params['authors'])
					.returning(Author)
				).all()

				for author in authors:
					book_author_params.append({ 'book_id': book[0].id, 'author_id': author.id})

				session.scalars(
					insert(BookAuthor)
					.values(book_author_params)
					.returning(BookAuthor)
				)
				session.commit()
			except:
				session.rollback()
				raise
			finally:
				session.close()

		return [book, authors]

	def update_book(self, id, update_params):
		with self.db as session:
			session.begin()
			try:
				book = session.scalars(
					update(Book)
					.where(Book.id == id)
					.values(title = update_params["title"])
					.returning(Book)
				).all()

				session.commit()
			except:
				session.rollback()
				raise
			finally:
				session.close()

		return book[0].id

	def delete_book(self, id):
		deleted_book = self.db.query(Book).filter(Book.id == id)
		book_author = self.db.query(BookAuthor).filter(BookAuthor.book_id == id)
		book_author.delete(synchronize_session=False)
		deleted_book.delete(synchronize_session=False)
		self.db.commit()

		return {'deleted_book' : deleted_book, 'success' : True}
