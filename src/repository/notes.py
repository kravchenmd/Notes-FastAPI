from sqlalchemy.orm import Session
from src.models import Note
from src.schemas.notes import NoteBase, NoteUpdate, NoteDone


async def get_all_notes(db: Session, skip: int, limit: int):
    all_notes = db.query(Note).offset(skip).limit(limit).all()
    return all_notes


async def get_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    return note


async def create_note(db: Session, note: NoteBase):
    new_note = Note(title=note.title, description=note.description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


async def update_note(db: Session, note_id: int, new_note: NoteUpdate):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.title = new_note.title
        note.description = new_note.description
        note.done = new_note.done
        db.commit()
    return note


async def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note


async def done_note(db: Session, note_id: int, new_note: NoteDone):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.done = new_note.done
        db.commit()
    return note
