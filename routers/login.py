from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from OAUTH.security import verify_password,create_access_token
from app.database import get_db
from crud import Manager
from schemas import Token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/login", tags=["Login"])
mananger = Manager()

@router.post("",response_model= Token, status_code=status.HTTP_200_OK)
def login(login_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = mananger.get_users_by_email(login_data.username,db)
    password_correct = verify_password(login_data.password,user.hashed_password)
    if user is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Invalid email or password"
        )
    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Invalid email or password"
        )
    token = create_access_token(user_id=user.user_id,role=user.role.value)
    return {
        "access_token": token,
        "token_type": "Bearer"
    }