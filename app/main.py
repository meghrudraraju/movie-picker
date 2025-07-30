from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models import user  # Import model so SQLAlchemy picks it up
from app.routes import user as user_routes  # Import router

app = FastAPI()

# ✅ CORS settings (adjust as needed for frontend port or deploy URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # if using Vite, else 8080 for Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create all tables
Base.metadata.create_all(bind=engine)

# ✅ Include your user-related routes
app.include_router(user_routes.router, prefix="/api")
