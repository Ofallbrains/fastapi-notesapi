from fastapi import APIRouter, HTTPException, status, Query
from datetime import date
from typing import List

from schemas import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

_notes: list[NoteResponse] = []
_next_id = 1

def _get_note_index(note_id: int) -> int:
    for i, note in enumerate(_notes):
        if note.id == note_id:
            return i
    return -1
    
@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(payload: NoteCreate):
    global _next_id
    
    note = NoteResponse(
        id=_next_id,
        title=payload.title,
        content=payload.content,
        created_at=date.today(),
    )
    _next_id += 1
    _notes.append(note)
    return note

@router.get(
    "",
    response_model=List[NoteResponse])
def list_notes(
    limit: int | None = Query(default=None, gt=0, description="Max notes to return"),
    title: str | None = Query(default=None, description="Filter notes containing this title text"),
):
    results = _notes
    
    if title:
        t = title.lower()
        results = [n for n in results if t in n.title.lower()]
        
    if limit is not None:
        results = results[:limit]
        
    return results

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    index = _get_note_index(note_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Note not found")
    return _notes[index]

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, payload: NoteUpdate):
    index = _get_note_index(note_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Note not found")
    existing = _notes[index]
    
    updated = NoteResponse(
        id=existing.id,
        title=payload.title if payload.title is not None else existing.title,
        content=payload.content if payload.content is not None else existing.content,
        created_at=existing.created_at,
    )
    _notes[index] = updated
    return updated

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int):
    index = _get_note_index(note_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Note not found")
    _notes.pop(index)
    return None