from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from db.database import get_db
from models.user import User, UserRole
from models.record import Record, RecordType
from api.dependencies import require_role
from api.services.document_analyzer import analyze_document_rule_based

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.VIEWER, UserRole.ANALYST, UserRole.ADMIN]))
):
    total_income = db.query(func.sum(Record.amount)).filter(Record.record_type == RecordType.INCOME).scalar() or 0.0
    total_expenses = db.query(func.sum(Record.amount)).filter(Record.record_type == RecordType.EXPENSE).scalar() or 0.0
    net_balance = total_income - total_expenses
    
    category_totals_query = db.query(
        Record.category, Record.record_type, func.sum(Record.amount)
    ).group_by(Record.category, Record.record_type).all()
    
    category_wise = []
    for cat, r_type, amount in category_totals_query:
        category_wise.append({
            "category": cat,
            "type": r_type.value,
            "total": amount
        })
        
    recent_records = db.query(Record).order_by(Record.date.desc()).limit(5).all()
    recent_activity = [
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.record_type.value,
            "category": r.category,
            "date": r.date.isoformat()
        } for r in recent_records
    ]
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "category_wise_totals": category_wise,
        "recent_activity": recent_activity
    }

@router.post("/reports/analyze")
async def analyze_report(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER]))
):
    if not file.filename.lower().endswith((".csv", ".pdf")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .csv and .pdf files are supported for rule-based analysis."
        )
    
    try:
        file_bytes = await file.read()
        analysis_markdown = analyze_document_rule_based(file_bytes, file.content_type, file.filename)
        return {"analysis": analysis_markdown}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze document: {str(e)}"
        )
