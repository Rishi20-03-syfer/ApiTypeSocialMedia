from pydantic import BaseModel

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

class PostResponse(Post):
    id:int
    class Config:
        orm_mode = True

