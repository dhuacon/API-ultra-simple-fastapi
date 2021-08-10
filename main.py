from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import  Optional, Dict
from uuid import uuid4
import json
import uvicorn


app = FastAPI()



class Post(BaseModel):
    id : Optional[str]
    post : Dict




def read_file():
    with open('posts.json', 'r', encoding='UTF-8') as post_file:
        return json.load(post_file)

def write_file(post_data):
    with open('posts.json', 'r+', encoding='UTF-8') as post_file:
        file_data = json.load(post_file)
        file_data.append(post_data)
        post_file.seek(0)
        json.dump(file_data, post_file, indent=4)
    post_file.close()


def update_file(post_data):
    with open('posts.json', 'w', encoding='UTF-8') as post_file:
        json.dump(post_data, post_file, indent=4)
    post_file.close()

 



@app.get('/posts')
def get_posts():
    return read_file()

@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid4())
    write_file(post.dict())
    return "saved"

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    posts = read_file()
    for post in posts:
        if post['id'] == post_id:
            return post

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    posts = read_file()
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            update_file(posts)
            return {"message": "Post has been deleted succesfully"}

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    posts = read_file()
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["post"]= updatedPost.dict()["post"]
            update_file(posts)
            return {"message": "Post has been updated succesfully"} 

