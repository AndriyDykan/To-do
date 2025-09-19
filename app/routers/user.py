from fastapi import APIRouter,Depends,HTTPException,status
from app.database.database import get_db
from app.schemas.user import UserGet,UserCreate
from app.models.user import User
from sqlalchemy.orm import Session
from app.security import hash_password,oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
router = APIRouter(prefix="/users", tags=["Users"])





def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


@router.post("/",response_model=UserGet)
def create_user(user:UserCreate ,db: Session = Depends(get_db)):
    db_user = User(username=user.username,email=user.email,password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 


@router.get("/me", response_model=UserGet)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
