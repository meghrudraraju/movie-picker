from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models import user, genre, movies,movie_features,user_interactions  # 👈 Add this line
from app.routes import user as user_routes  # Import router

app = FastAPI()

# ✅ CORS settings (adjust as needed for frontend port or deploy URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
		   "http://localhost:5174",
		   "https://what2watch-me1v.onrender.com"],  # if using Vite, else 8080 for Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create all tables
Base.metadata.create_all(bind=engine)

# ✅ Include your user-related routes
app.include_router(user_routes.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))  # Render sets PORT env var
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
