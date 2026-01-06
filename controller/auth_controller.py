# File: controller/auth_controller.py

from fastapi import APIRouter, HTTPException, Depends, status
# FIX: Ensure AuthResponse is imported here. 
# You need to define AuthResponse in models/user_model.py first!
from models.user_model import UserRegister, UserLogin, UserOut, Token, AuthResponse
from database import get_user_collection # Assuming this is the correct path

# --- DUMMY TOKEN FUNCTION (INSECURE) ---
def create_dummy_token(email: str) -> str:
    """Returns a dummy token based on email, NOT secure!"""
    return f"DUMMY_TOKEN_FOR_{email}"

# --- 1. Router Initialization ---
auth_router = APIRouter(tags=["Authentication"])

# --- 2. Dependencies ---
def get_collection():
    """Returns the user collection object."""
    return get_user_collection()

# --- 3. Authentication Endpoints ---

@auth_router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, users_collection = Depends(get_collection)):
    """Simple registration: stores user details including username and role."""
    
    # 1. Check if user already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    # 2. Prepare data for MongoDB
    user_document = {
        "email": user_data.email,
        "password": user_data.password, # Storing plain text password (INSECURE)
        "username": user_data.username,
        "role": user_data.role
    }

    # 3. Insert into DB
    result = await users_collection.insert_one(user_document)
    
    # 4. Fetch the newly created user (for the response)
    new_user = await users_collection.find_one({"_id": result.inserted_id})
    
    # 5. Return the clean UserOut response model
    return UserOut(
        id=str(new_user["_id"]), 
        email=new_user["email"],
        username=new_user.get("username"),
        role=new_user["role"]
    )


@auth_router.post("/login", response_model=AuthResponse) # <--- FIX 1: Change response_model to AuthResponse
async def login(user_data: UserLogin, users_collection = Depends(get_collection)):
    """Handles login, verifies password (insecurely), and returns token + role for client-side redirection."""
    
    # 1. Find user by email
    db_user = await users_collection.find_one({"email": user_data.email})
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    # 2. Verify password: Simple string comparison (INSECURE)
    if user_data.password != db_user.get("password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    # 3. Create Dummy Token
    access_token = create_dummy_token(user_data.email)
    
    # 4. Return the token, email, and the role
    # <--- FIX 2: Return AuthResponse with role and email --->
    return AuthResponse(
        access_token=access_token,
        email=db_user["email"],
        role=db_user["role"] 
    )