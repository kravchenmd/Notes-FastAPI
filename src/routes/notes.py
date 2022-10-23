from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from db.connect import get_db
from src.repository import notes
from src.schemas.notes import NoteBase, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])
async def get_all_notes(db: Session = Depends(get_db)):
    all_notes = await notes.get_all_notes(db)
    return all_notes


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    note = await notes.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with ID {note_id} not found")
    return note


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteResponse)  # change return code to make post method idempotent
async def create_note(note: NoteBase, db: Session = Depends(get_db)):
    note = await notes.create_note(db, note)
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    note = await notes.update_note(db, note_id, note)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with ID {note_id} not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = await notes.delete_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with ID {note_id} not found")
    return note
