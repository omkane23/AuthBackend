from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # NEW IMPORT
from config.settings import settings
from database import connect_to_mongo, close_mongo_connection
from controller.auth_controller import auth_router

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.VERSION
)

# --- 0. CORS Middleware Configuration (THE FIX) ---
origins = [
    # Replace 5173 with your actual front-end port if it changes (Vite default is often 5173)
    "*" # Allow all origins for testing; change to specific origins in production
    # Add any other frontend addresses here, like a staging server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# --------------------------------------------------

# --- 1. DB Connection Events ---
@app.on_event("startup")
async def startup_db_client():
    """Run connection logic when the application starts."""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Run connection logic when the application shuts down."""
    await close_mongo_connection()

# --- 2. Include Routers (API Endpoints) ---
app.include_router(auth_router, prefix="/api/auth")

# To run: uvicorn main:app --reload