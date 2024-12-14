import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://127.0.0.1:5000';


function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPass, setConfirmPass] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const navigate = useNavigate();

  const clear = async () => {
    setPassword('');
    setConfirmPass('')
  }
  // User registration
  const register = async () => {
    try {
      await axios.post(`${API_BASE_URL}/user/create`, { username, password, confirmPass });
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
        type={showPassword ? 'text' : 'password'}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ marginRight: '10px'}}
      />
      <button type="button"
        onMouseDown={() => setShowPassword(true)} // Show password when button is held
        onMouseUp={() => setShowPassword(false)} // Hide password when button is released
        onMouseLeave={() => setShowPassword(false)}> Show Password </button>
      <br />
      <label> Confirm Password: </label>
      <input
        type={showConfirmPassword ? 'text' : 'password'}
        value={confirmPass}
        onChange={(e) => setConfirmPass(e.target.value)}
        style={{ marginBottom: '10px', marginRight: '10px'
        }}
      />
      <button type="button"
        onMouseDown={() => setShowConfirmPassword(true)} // Show password when button is held
        onMouseUp={() => setShowConfirmPassword(false)} // Hide password when button is released
        onMouseLeave={() => setShowConfirmPassword(false)}> Show Password </button>
      <br />
      <label> Password must: 
        <ul>
            <li>Be at least 8 characters long</li>
            <li>Contain a special character </li>
            <li>Contain at least one uppercase letter</li>
        </ul>
         </label>
      <br />
      <button onClick={() => {register();clear()}}>Register</button>

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
