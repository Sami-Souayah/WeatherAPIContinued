import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://127.0.0.1:5000';


function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();


  // User registration
  const register = async () => {
    try {
      await axios.post(`${API_BASE_URL}/user/create`, { username, password });
      setError('');
      alert('Registration successful! You can now log in.');
      
      // Navigate to the login page after successful registration
      navigate('/');  // This assumes the login page is at the root ("/")
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  return (
    <div>
      <h2>User Registration</h2>
      <label>Username: </label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <br />
      <label>Password: </label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <button onClick={register}>Register</button>

      {error && (
        <div style={{ color: 'red' }}>
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default Register;
