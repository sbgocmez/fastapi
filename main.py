from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

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
    print(payLoad['device '])
    return {
        "Send successfuly",
    }