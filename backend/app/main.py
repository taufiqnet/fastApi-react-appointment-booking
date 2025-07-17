from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.db.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Appointment Booking System",
    version="1.0.0"
)

# ✅ Allow frontend to access the backend
origins = [
    "http://localhost:3000",  # frontend dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # or explicitly ["POST", "GET"]
    allow_headers=["*"],      # or explicitly ["Authorization", "Content-Type"]
)

# Add routes
app.include_router(api_router, prefix="/api/v1")



@app.on_event("startup")
def on_startup():
    # Create database tables on startup
    create_db_and_tables()
