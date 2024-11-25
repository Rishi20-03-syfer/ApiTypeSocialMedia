from fastapi import FastAPI, HTTPException, status, Response,Depends
from pydantic import BaseModel
import psycopg
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

connection = psycopg.connect("dbname = fastapi user=postgres password=R!$H!2003")
cursor = connection.cursor()

class Post(BaseModel):
    id: int = 0
    title: str
    content: str
    published: bool = True

@app.get("/")
def root():
    return {"data": "Server is running.."}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    return {"message":"success"}

@app.get("/posts")
def get_posts():
    cursor.execute("select * from social_media;")
    user_posts = cursor.fetchall()
    return {"Posts": user_posts}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("insert into social_media (title,content,published) values(%s,%s,%s)",(post.title,post.content,post.published))
    connection.commit()
    return {"message": "Post created successfully!!"}



@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute("select * from social_media where id = %s",(str(id),))
    required_post = cursor.fetchone()
    if not required_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The requested post id {id} not found")

    return {"message": required_post}



@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        cursor.execute("delete from social_media where id = %s ",(str(id),))
        connection.commit()
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id {id} not found.")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    try:
        cursor.execute(f"update social_media set title=%s, content=%s where id = %s;",(post.title,post.content,str(id),))
        connection.commit()
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found.")
