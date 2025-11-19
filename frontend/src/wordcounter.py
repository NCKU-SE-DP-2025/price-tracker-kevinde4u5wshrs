from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class string(BaseModel):
    words: List[str]

class length(BaseModel):
    word: str
    length: int

@app.post("/api/v1/word-length-calculator", response_model=List[length])
def calculate_word_lengths(data: string):
    result = [{"word": word, "length": len(word)} for word in data.words]
    return result
