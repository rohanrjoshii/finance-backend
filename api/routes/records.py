from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from db.database import get_db
from models.user import User, UserRole
from models.record import Record, RecordType
from schemas.record import RecordCreate, RecordResponse, RecordUpdate
from api.dependencies import get_current_user, require_role

router = APIRouter(prefix="/records", tags=["records"])

@router.post("/", response_model=RecordResponse)
def create_record(
    record_in: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    db_record = Record(
        **record_in.dict(),
        author_id=current_user.id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/", response_model=List[RecordResponse])
def get_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    record_type: Optional[RecordType] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Record)
    
    if record_type:
        query = query.filter(Record.record_type == record_type)
    if category:
        query = query.filter(Record.category == category)
    if start_date:
        query = query.filter(Record.date >= start_date)
    if end_date:
        query = query.filter(Record.date <= end_date)
        
    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_update: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
        
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return {"detail": "Record deleted successfully"}
