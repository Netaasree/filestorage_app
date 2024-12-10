import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [file, setFile] = useState(null);

  const handleRegister = async () => {
    const response = await axios.post('http://localhost:5000/register', { username, password });
    alert(response.data.msg);
  };

  const handleLogin = async () => {
    const response = await axios.post('http://localhost:5000/login', { username, password });
    alert(response.data.msg);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('http://localhost:5000/upload', formData);
    alert(response.data.msg);
  };

  return (
    <div className="App">
      <h1>Online File Storage</h1>
      <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleFileUpload}>Upload File</button>
    </div>
  );
}

export default App;
