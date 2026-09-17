from schemas import LoginRequest,Token
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from OAUTH.security import verify_password,create_access_token
from app.database import get_db
from crud import Manager


router = APIRouter(prefix="/Login", tags=["Login"])
manager = Manager()

@router.post('/',response_model=Token,status_code=status.HTTP_200_OK)
def Login(login_data:LoginRequest,db:Session= Depends(get_db)):
    user = manager.get_users_by_email(login_data.email,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid email or password"
        )
    correct_password = verify_password(login_data.password,user.hashed_password)
    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
        )
    token = create_access_token(user.user_id,user.role.value)
    return {
        "access_token": token,
        "token_type": "bearer"
    }