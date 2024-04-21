import React, { useState } from 'react';
import axios from 'axios';

function RecordAttendance() {
  const [attendance, setAttendance] = useState({
    student_id: '',
    in_full_uniform: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAttendance({ ...attendance, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/attendance/', attendance);
      alert('Attendance recorded successfully');
    } catch (error) {
      console.error('Error recording attendance:', error);
    }
  };

  return (
    <div>
      <h2>Record Attendance</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="student_id" placeholder="Student ID" onChange={handleChange} required />
        <select name="in_full_uniform" onChange={handleChange} required>
          <option value="">-- Select Uniform Status --</option>
          <option value="true">In Full Uniform</option>
          <option value="false">Not in Full Uniform</option>
        </select>
        <input type="submit" value="Record Attendance" />
      </form>
    </div>
  );
}

export default RecordAttendance;
