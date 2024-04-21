import React from 'react';
import './App.css';
import RegisterStudent from './components/RegisterStudent';
import RecordAttendance from './components/RecordAttendance';

function App() {
  return (
    <div className="App">
      <RegisterStudent />
      <RecordAttendance />
    </div>
  );
}

export default App;
