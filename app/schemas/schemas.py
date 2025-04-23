from pydantic import BaseModel
from datetime import date

class DocumentResponse(BaseModel):
    path: str
    date: date

class MessageResponse(BaseModel):
    message: str

class TextResponse(BaseModel):
    text: str