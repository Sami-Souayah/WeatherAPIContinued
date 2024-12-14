import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const API_BASE_URL = 'http://127.0.0.1:5000';


function UpdatePass() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [newPassword,setNewPassword] = useState('');
    const [error, setError] = useState('');   

    const navigate = useNavigate();


    const Update = async () => {
        try {
          await axios.post(`${API_BASE_URL}/user/update_password/`, { username, password,newPassword });
          setError(''); 
          alert('Password successfully updated!');
          navigate('/');  
        } catch (err) {
          setError(err.response ? err.response.data.error : 'An error occurred');
        }
      };

      return (
        <div>
          <h2>Update Password</h2>
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
          <label>New Password: </label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <br />
          <button onClick={Update}>Update Password</button>
    
          {error && (
            <div style={{ color: 'red' }}>
              <h2>Error</h2>
              <p>{error}</p>
            </div>
          )}
        </div>
      );
    }
    
    export default UpdatePass;
