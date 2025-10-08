from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/me")

def read_root():
    return {
    "name": "王浚宇",
    "student_id": "F74146830"
}