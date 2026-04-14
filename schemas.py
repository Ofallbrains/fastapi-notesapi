from pydantic import BaseModel, Field
from datetime import date

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    contnet: str = Field(min_length=1, max_length=5000)
    
class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: date