from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/rectangle-area")
def read_root(width: int, height: int):
    return {width * height}