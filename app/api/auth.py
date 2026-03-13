from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from app.core.config import get_settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.generated_models import Users
from app.schemas.user import Token, TokenData, UserCreate, UserResponse

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Khong the xac thuc nguoi dung",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return TokenData(email=payload.get("sub"), role=payload.get("role"))
    except jwt.PyJWTError as exc:
        raise _credentials_exception() from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Users:
    token_data = _decode_token(token)
    if not token_data.email:
        raise _credentials_exception()

    user = db.query(Users).filter(Users.email == token_data.email).first()
    if user is None:
        raise _credentials_exception()

    return user


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(Users).filter(Users.email == user_in.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email nay da duoc dang ky.")

    new_user = Users(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        company_name=user_in.company_name,
        role="user",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoac mat khau khong chinh xac",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}