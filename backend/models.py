from pydantic import BaseModel
from typing import List, Optional

class Student(BaseModel):
    id: Optional[int]
    student_name: str
    roll_number: int
    semester: int
    tutor_name: str
    cgpa: float
    face_encoding: List[float]

class Attendance(BaseModel):
    id: Optional[int]
    student_id: int
    in_full_uniform: bool
    attendance_date: Optional[str]

# Example face encoding: [0.1, 0.2, 0.3, ..., 0.99]
