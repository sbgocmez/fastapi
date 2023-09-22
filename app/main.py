from fastapi import FastAPI, Response, status
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of 1 ", "content":"content of p", "id":1}]
# path operation
# function and decorator
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/devices")
def get_userDataDevice():
    return {"device data": "Mobile"}

@app.post("/devices")
def send_userDataDevice(payLoad: dict = Body(...)):
    print(payLoad['device'])
    return {
        "Send successfuly",
    }
    
@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def send_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data: " : post_dict}

def find_by_id(id):
    for i in range(len(my_posts)):
        if (my_posts[i]['id'] == id):
            return my_posts[i]

@app.get("/posts/{id}")
def get_post(id: int):
    print(int(id))
    post = find_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id ")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f'post with id {id} not found'}
    return {"data": find_by_id(id)}


def find_index_post(id):
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == id:
            return i

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    
    if index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id ")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    print(index)
    print(index)
    if index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id ")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {'message: ': post_dict}

