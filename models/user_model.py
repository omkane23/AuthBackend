# File: models/user_model.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal

# Define the allowed roles for type checking and validation
UserRole = Literal["student", "teacher", "admin"]


### --- Database Model (Used Internally) ---
# This defines how the user object is stored in MongoDB
class UserInDB(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str 
    username: Optional[str] = None  # Optional username field
    role: UserRole                 # Mandatory role field

    class Config:
        from_attributes = True


### --- Request Body Schemas ---

class UserRegister(BaseModel):
    """Schema for user registration input."""
    email: EmailStr
    password: str
    username: Optional[str] = None  # Optional field for registration
    # Mandatory role field, must be one of the defined literals
    role: UserRole = "student"      # Default role to 'student' if not provided
    
   




class UserLogin(BaseModel):
    """Schema for user login input (only needs email and password)."""
    email: EmailStr
    password: str

# --- Response Schemas ---

class Token(BaseModel):
    """Schema for the token response."""
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    """Schema for user details returned in a successful response."""
    id: str
    email: EmailStr
    username: Optional[str] = None
    role: UserRole
    # <--- YOU MUST ADD/ENSURE THIS CLASS IS PRESENT AND CORRECT --->
class AuthResponse(Token):
    """The complete response returned after a successful login."""
    role: UserRole
    email: EmailStr

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str] = None
    role: UserRole