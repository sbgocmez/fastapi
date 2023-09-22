from fastapi import FastAPI, Response, status
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None
    
class Track(BaseModel):
    device: str
    platform: str
    timestamp: str
    language: str
    

# burayi while a almayi dusunebiliriz
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='busra123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    
    print("Database connection is succesful!")
except Exception as dbConnectionError:
    print("Connecting to database was failed.")
    print(dbConnectionError)
    #time.sleep(3)


my_posts = [{"title": "title of 1 ", "content":"content of p", "id":1}]
# path operation
# function and decorator
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tracks")
def get_tracks():
    cursor.execute("""SELECT * FROM public."Tracks" """)
    tracks = cursor.fetchall()
    print(tracks)
    return {"device data": tracks}

@app.post("/tracks", status_code=status.HTTP_201_CREATED)
def create_tracks(track: Track):
    variables = (track.device, track.platform, track.timestamp, track.language)
    print(variables)
    cursor.execute("""INSERT INTO public."Tracks" (device, platform, timestamp, language) VALUES (%s, %s, %s, %s) RETURNING *""", (track.device, track.platform, track.timestamp, track.language))
    new_track = cursor.fetchone()
    conn.commit()
    return {"added": new_track}

@app.get("/tracks/{id}")
def get_one_track(id):
    cursor.execute("""SELECt * FROM public."Tracks" where id = %s""", (id,))
    track = cursor.fetchone()
    
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id ")
    
    return(track)
    

@app.delete("/tracks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(id:int):
    cursor.execute("""DELETE FROM public."Tracks" WHERE id=%s returning *""", (str(id)))
    deleted_track = cursor.fetchone()
    conn.commit()
    
    if deleted_track == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id ")
    return({"data ": "deleted_track"})

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

