from typing import Annotated, List, Dict, Optional
from fastapi import Depends
from models import BookRepository as Repository
from fastapi.encoders import jsonable_encoder


def init_response_model(model_result):
	json_response = []
	for data in model_result:
		json_result = jsonable_encoder(data)
		json_response.append(json_result)

	return json_response

class BookService:
	def __init__(self, r: Annotated[Repository, Depends(Repository)]):
		self.repository = r

	def book_records(self, id: Optional[int] = None):
		model_data = self.repository.get_books(id)

		if not model_data: return None
		
		json_response = []
		
		for book, authors in model_data:
			book_json = init_response_model([book])[0]
			book_json['authors'] = authors
			json_response.append(book_json)

		return json_response[0] if id else json_response

	def create_book_record(self, request_params):
		book, authors = self.repository.create_book(request_params)
		
		json_result = init_response_model(book)[0]
		json_result['authors'] = init_response_model(authors)
		
		return json_result

	def update_book_record(self, id, update_params):
		book_id = self.repository.update_book(id, update_params)
				
		return self.book_records(book_id)

	def delete_book_record(self, id):
		return self.repository.delete_book(id)