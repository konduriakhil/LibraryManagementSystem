import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Define the allowed origins
origins = [
    "http://localhost:3000",  # Add the frontend URL you want to allow
    "http://frontend:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api/v1/info")
def get_secret_details():
    details = dict()
    details['SECRET'] = auth.SECRET_KEY
    details['ALGORITHM'] = auth.ALGORITHM
    return json.dumps(details)




@app.post("/api/v1/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): The user data to be created.
        db (Session): The database session.

    Returns:
        schemas.User: The created user entry.

    Raises:
        HTTPException: If the username is already registered.
    """
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(**user.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/v1/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials.
        db (Session): The database session.

    Returns:
        schemas.Token: The access and refresh tokens.

    Raises:
        HTTPException: If the authentication fails.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username, "user_type": user.user_type.value})
    refresh_token = auth.create_refresh_token(data={"sub": user.username, "user_type": user.user_type.value})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/api/v1/token/refresh", response_model=schemas.Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh the access token using a valid refresh token.

    Args:
        refresh_token (str): The refresh token.
        db (Session): The database session.

    Returns:
        schemas.Token: The new access and refresh tokens.

    Raises:
        HTTPException: If the refresh token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_type: str = payload.get("user_type")
        token_type: str = payload.get("type")
        if username is None or token_type != "refresh" or user_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.user_type.value != user_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or user type mismatch",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username, "user_type": user.user_type.value})
    new_refresh_token = auth.create_refresh_token(data={"sub": user.username, "user_type": user.user_type.value})
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@app.get("/api/v1/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Get the current authenticated user's information.

    Args:
        current_user (schemas.User): The current authenticated user.

    Returns:
        schemas.User: The current user's information.
    """
    return current_user

@app.get("/api/v1/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Get a list of users.

    Args:
        skip (int): The number of users to skip.
        limit (int): The maximum number of users to return.
        db (Session): The database session.
        current_user (schemas.User): The current authenticated user.

    Returns:
        list[schemas.User]: A list of user entries.
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/api/v1/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Get a specific user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.
        current_user (schemas.User): The current authenticated user.

    Returns:
        schemas.User: The user entry.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/api/v1/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Update a user's information.

    Args:
        user_id (int): The ID of the user to update.
        user (schemas.UserCreate): The updated user data.
        db (Session): The database session.
        current_user (schemas.User): The current authenticated user.

    Returns:
        schemas.User: The updated user entry.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude={"password"}).items():
        setattr(db_user, key, value)
    if user.password:
        db_user.hashed_password = auth.get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/api/v1/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): The database session.
        current_user (schemas.User): The current authenticated user.

    Returns:
        schemas.User: The deleted user entry.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user