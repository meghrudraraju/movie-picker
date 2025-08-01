from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.user import UserCreate, LoginRequest
from app.utils.auth import verify_password, create_access_token, get_current_user
from app.models.user import User
from app.db.database import SessionLocal
from app.crud import user as crud_user

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Signup Route
# ----------------------------
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud_user.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = crud_user.create_user(db, user)
    return {"message": "User created", "user_id": new_user.id}

# ----------------------------
# Login Route
# ----------------------------
@router.post("/login")
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, login_req.email)
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

# ----------------------------
# Get User Profile
# ----------------------------
@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    print("Fetched user profile:")
    print("User ID:", current_user.id)
    print("Onboarding:", current_user.has_completed_onboarding)
    print("Genres:", current_user.preferred_genres)
    print("Languages:", current_user.preferred_languages)
    print("Preferred:", current_user.preferred_mood)

    return {
        "user_id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "dob": current_user.dob,
        "pincode": current_user.pincode,
        "username": current_user.username,
        "hasCompletedOnboarding": current_user.has_completed_onboarding,
        "genres": current_user.preferred_genres,
        "languages": current_user.preferred_languages,
        "preferred": current_user.preferred_mood
    }
# ----------------------------
# Update Profile (Onboarding, Preferences)
# ----------------------------
class OnboardingUpdate(BaseModel):
    hasCompletedOnboarding: Optional[bool]
    genres: Optional[List[str]]
    languages: Optional[List[str]]
    preferred: Optional[str]

@router.patch("/me")
def update_profile(
    update: OnboardingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update.hasCompletedOnboarding is not None:
        user.has_completed_onboarding = update.hasCompletedOnboarding

    if update.genres is not None:
        user.preferred_genres = ",".join(update.genres)

    if update.languages is not None:
        user.preferred_languages = ",".join(update.languages)

    if update.preferred is not None:
        user.preferred_mood = update.preferred

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated",
        "user": {
            "id": user.id,
            "hasCompletedOnboarding": user.has_completed_onboarding,
            "genres": user.preferred_genres,
            "languages": user.preferred_languages,
            "preferred": user.preferred_mood
        }
    }

#----------------------
# Get Health from Backend
#------------------------
@router.get("/health")
def health_check():
    return {"status": "ok"}
