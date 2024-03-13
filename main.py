import logging
from fastapi import FastAPI
from pydantic import BaseModel
import schema
from router import books

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = FastAPI()
app.include_router(books.router)
