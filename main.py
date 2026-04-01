from fastapi import FastAPI
from db.database import engine, Base
from api.routes.auth import router as auth_router
from api.routes.users import router as users_router
from api.routes.records import router as records_router
from api.routes.dashboard import router as dashboard_router
from web.routes import router as web_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard Backend",
    description="Backend API for Finance Dashboard System",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(records_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(web_router)

from fastapi.staticfiles import StaticFiles
import os

os.makedirs("static", exist_ok=True)
app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to Finance Dashboard API. See /docs for the API documentation."}
