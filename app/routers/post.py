from typing import Optional, List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model = List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                   limit: int = 10, skip: int = 0, search :Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # .join() -> by default left inner join.
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model = schemas.PostOut)
def get_post_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (id,))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first() # we can do .all() but it will scan the entire DB even though id is unique. Hence give first occurence.
    

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found.")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized Access")
    return post

@router.post("/", response_model= schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), status_code = status.HTTP_204_NO_CONTENT):
    # cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized Access")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), statu_code = status.HTTP_201_CREATED):
    # cursor.execute("""UPDATE POSTS SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized Access")

    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()

    return post_query.first()

