from pydantic import BaseModel

class User_Account(BaseModel):
    id: int
    username: str
    password: str