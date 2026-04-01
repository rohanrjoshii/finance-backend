from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from models.user import User
from models.record import Record, RecordType
from api.dependencies import get_current_user

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

def get_auth_user(request: Request, db: Session):
    try:
        return get_current_user(request=request, db=db, token="")
    except HTTPException:
        return None

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.get("/logout")
def logout(response: RedirectResponse):
    resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie("access_token")
    return resp

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db)):
    user = get_auth_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    total_income = db.query(func.sum(Record.amount)).filter(Record.record_type == RecordType.INCOME).scalar() or 0.0
    total_expenses = db.query(func.sum(Record.amount)).filter(Record.record_type == RecordType.EXPENSE).scalar() or 0.0
    net_balance = total_income - total_expenses
    raw_runway = (net_balance / (total_expenses or 1)) * 12 if total_expenses and net_balance > 0 else 0
    runway = min(120.0, raw_runway)
    
    recent_records = db.query(Record).order_by(Record.date.desc()).limit(10).all()
    
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "request": request, 
        "user": user,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "runway": runway,
        "records": recent_records
    })

@router.get("/transactions", response_class=HTMLResponse)
def transactions_page(request: Request, db: Session = Depends(get_db)):
    user = get_auth_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    return templates.TemplateResponse(request=request, name="transactions.html", context={
        "request": request,
        "user": user
    })

@router.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request, db: Session = Depends(get_db)):
    user = get_auth_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    return templates.TemplateResponse(request=request, name="reports.html", context={
        "request": request,
        "user": user
    })

@router.get("/logs", response_class=HTMLResponse)
def logs_page(request: Request, db: Session = Depends(get_db)):
    user = get_auth_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    recent_records = db.query(Record).order_by(Record.date.desc()).limit(25).all()
        
    return templates.TemplateResponse(request=request, name="logs.html", context={
        "request": request,
        "user": user,
        "records": recent_records
    })
