from fastapi import FastAPI, websockets,HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()

class books(BaseModel):
    author:str
    year: int

list_of_books:dict[BaseModel, books] = {}

@app.get("/")
def get_something():
    return
