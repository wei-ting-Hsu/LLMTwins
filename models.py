from  pydantic import BaseModel

class regUser(BaseModel):
    name: str
    description: str

class getUser(BaseModel):
    name: str

class prompt(BaseModel):
    role: str
    message: str