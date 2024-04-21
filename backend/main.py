from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
import json

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

students = []

@app.get("/students/")
async def read_students():
    return {"students": students}

@app.post("/students/")
async def create_student(student: dict):
    face_encoding_str = student.pop("face_encoding")
    student["face_encoding"] = json.loads(base64.b64decode(face_encoding_str))
    students.append(student)
    return {"message": "Student created successfully"}
