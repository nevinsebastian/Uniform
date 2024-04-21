import React, { useState } from 'react';
import axios from 'axios';

function RegisterStudent() {
  const [student, setStudent] = useState({
    student_name: '',
    roll_number: '',
    semester: '',
    tutor_name: '',
    cgpa: '',
    face_encoding: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setStudent({ ...student, [name]: value });
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      setStudent({ ...student, face_encoding: reader.result });
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/students/', student, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      alert('Student registered successfully');
    } catch (error) {
      console.error('Error registering student:', error);
    }
  };

  return (
    <div>
      <h2>Register Student</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="student_name" placeholder="Student Name" onChange={handleChange} required />
        <input type="text" name="roll_number" placeholder="Roll Number" onChange={handleChange} required />
        <input type="text" name="semester" placeholder="Semester" onChange={handleChange} required />
        <input type="text" name="tutor_name" placeholder="Tutor Name" onChange={handleChange} required />
        <input type="text" name="cgpa" placeholder="CGPA" onChange={handleChange} required />
        <input type="file" accept=".json" onChange={handleFileChange} required />
        <input type="submit" value="Register" />
      </form>
    </div>
  );
}

export default RegisterStudent;
