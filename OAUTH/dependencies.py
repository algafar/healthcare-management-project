from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from OAUTH.security import SECRET_KEY,ALGORITHM
from jose import jwt,JWTError
from crud import Manager


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
manager = Manager()


def get_current_user(token:str = Depends(oauth_scheme),db:Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials"
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = manager.get_users_by_id(int(user_id),db)
    if user is None:
        raise credential_exception
    return user



