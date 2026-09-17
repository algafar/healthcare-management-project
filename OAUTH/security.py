from datetime import datetime,timezone,timedelta
from pwdlib import PasswordHash
from app.config import setting
from jose import jwt




SECRET_KEY = setting.SECRET_KEY

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended() 


def hashed_password(password:str)-> str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)-> bool:
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(user_id:str,role:str)-> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": int(user_id),
        "role": role,
        "exp": expire
    }

    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

