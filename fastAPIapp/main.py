from fastapi import FastAPI
from schemas import User_Account

app = FastAPI()


@app.get('/')
def index(request: User_Account):
    return request