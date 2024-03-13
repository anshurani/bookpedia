from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Path, Depends
from starlette import status
import schema
from services import BookService as Service
import logging

router = APIRouter(
	prefix='/books',
	tags=['Books']
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# index
@router.get('/', response_model=List[schema.BookSchema])
def book_records(s: Annotated[Service, Depends(Service)]):
	books = s.book_records()
	return books

# show
@router.get('/{id}', response_model=schema.BookSchema, status_code=status.HTTP_200_OK)
def get_one_book(id: int, s: Annotated[Service, Depends(Service)]):
	book = s.book_records(id)

	if book is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
	return book

# create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.BookSchema)
def create_book(post_book:schema.CreateBook, s: Annotated[Service, Depends(Service)]):
	new_book = s.create_book_record(post_book.dict())
	return new_book

#update
@router.put('/books/{id}', response_model=schema.BookSchema)
def update_book(updated_book:schema.CreateBook, id:int, s: Annotated[Service, Depends(Service)]):
	updated_book =  s.update_book_record(id, updated_book.dict())

	if updated_book is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
	
	return updated_book

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_book(id:int, s: Annotated[Service, Depends(Service)]):
	deleted_book = s.delete_book_record(id)

	if deleted_book['deleted_book'] is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
							detail=f"The id: {id} you requested for does not exist")






