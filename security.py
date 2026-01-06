from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config.settings import settings

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hash."""
    # Truncate the password before verification to match the hashing process
    truncated_password = plain_password[:72].encode('utf-8')
    return pwd_context.verify(truncated_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Returns the hash of a plaintext password, truncating if necessary."""
    # --- CRITICAL FIX: Truncate password to 72 bytes (characters) ---
    truncated_password = password[:72].encode('utf-8')
    
    # We pass the truncated, encoded bytes to the hash function
    return pwd_context.hash(truncated_password)

# --- JWT Token Utilities ---
def create_access_token(data: dict) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# You would add a decode/verification function here later for protected routes