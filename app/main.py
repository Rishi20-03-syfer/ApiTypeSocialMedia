from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
import psycopg
from . import models,Schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from typing import List
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connection = psycopg.connect("dbname = fastapi user=postgres password=R!$H!2003")
# cursor = connection.cursor()


# class PostSchema(BaseModel):
#     title: str
#     content: str
#     published: bool = True


@app.get("/")
def root():
    return {"data": "Server is running.."}


@app.get("/posts",response_model=List[Schemas.PostResponse] )
def get_posts(db: Session = Depends(get_db)):
    # user_posts = cursor.execute("select * from social_media;")
    user_posts = db.query(models.Post).all()
    return user_posts


@app.post("/createpost", status_code=status.HTTP_201_CREATED,response_model=Schemas.PostResponse )
def create_post(new_post: Schemas.Post,db:Session=Depends(get_db)):
    new_post = models.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    return new_post


@app.get("/post/{id}",response_model=Schemas.PostResponse)
def get_post(id: int,db:Session=Depends(get_db)):
    # cursor.execute("select * from social_media where id = %s", (str(id),))
    # required_post = cursor.fetchone()
    required_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not required_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The requested post id {id} not found")

    return required_post


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
    #     cursor.execute("delete from social_media where id = %s ", (str(id),))
    #     connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}",response_model=Schemas.PostResponse)
def update_post(id: int, post: Schemas.Post,db:Session=Depends(get_db)):
    # try:
        # cursor.execute(f"update social_media set title=%s, content=%s where id = %s;",
        #                (post.title, post.content, str(id),))
        # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found.")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return
