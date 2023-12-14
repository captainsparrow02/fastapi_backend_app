from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=['Users']
)

@router.post('/users', response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),statu_code = status.HTTP_201_CREATED):
    user.password = utils.hash(user.password)
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found.")
    return user