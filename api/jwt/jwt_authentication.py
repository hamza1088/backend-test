from fastapi import HTTPException, APIRouter, Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$F/8sQrYj5b5JLRlXUqMoje7n7fJgQIJZl/Cl3N4vYJnElH8HQ4iNi",
    }
}

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify user credentials and generate a token
def authenticate_user(user: UserLogin):
    if user.username not in fake_users_db:
        return None

    # Verify the password
    stored_password_hash = fake_users_db[user.username]["password"]
    # if not pwd_context.verify(user.password, stored_password_hash):
    #     return None

    # Generate a token for the user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "exp": datetime.utcnow() + access_token_expires}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login/", response_model=Token)
async def login_for_access_token(user: UserLogin):
    token = authenticate_user(user)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
