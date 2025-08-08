from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age_group: str   # e.g., "teen", "young_adult", "adult", "senior"
    location: str    # e.g., "Bangalore", "Delhi"
    password: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    hasCompletedOnboarding: bool
    preferredGenres: Optional[str]
    preferredLanguages: Optional[str]
    preferredMood: Optional[str]

    class Config:
        orm_mode = True

class MoodUpdate(BaseModel):
    preferred_mood: str

class UserUpdateRequest(BaseModel):
    hasCompletedOnboarding: Optional[bool]
    preferredGenres: Optional[List[int]]
    preferredLanguages: Optional[List[str]]
    preferredMood: Optional[str]
