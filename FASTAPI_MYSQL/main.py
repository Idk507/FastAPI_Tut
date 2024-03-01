from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

@app.post("/users/", status_code=201)
async def create_user(user: UserBase, db: Session = db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    
@app.post("/posts/", status_code=201)
async def create_post(post : PostBase,db : db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
@app.get("/posts/{post_id}",status_code = 200)
async def read_post(post_id:int,db:db_dependency):
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        HTTPException(status_code=404,detail="Post not found")
    return post
@app.delete("/posts/{post_id}",status_code=200)
async def delete_post(post_id:int,db:db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message":"Post deleted successfully"}

@app.get("/users/{user_id}",status_code= 200)
async def read_user(user_id :int,db:db_dependency):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user
models.Base.metadata.create_all(bind=engine)
