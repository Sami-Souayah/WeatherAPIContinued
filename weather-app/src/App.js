import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState('');
  const [locationName, setLocationName] = useState('');
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // User login
  const login = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/user/login`, {
        username,
        password,
      });
      setUserId(response.data.user_id);
      setIsLoggedIn(true);
      setError('');
      alert('Login successful!');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // User registration
  const register = async () => {
    try {
      await axios.post(`${API_BASE_URL}/user/create`, {
        username,
        password,
      });
      setError('');
      alert('Registration successful! You can now log in.');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Fetch hourly forecast
  const fetchHourlyForecast = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/forecast/hourly/${locationName}`);
      setForecastData(response.data.hourly_forecast);
      setError('');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Fetch daily forecast
  const fetchDailyForecast = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/forecast/daily/${locationName}`);
      setForecastData(response.data.daily_forecast);
      setError('');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Fetch weather for all favorites
  const fetchFavoritesWeather = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/weather/favorites`, {
        params: { user_id: userId },
      });
      setForecastData(response.data.locations);
      setError('');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Add a favorite location
  const addFavorite = async () => {
    try {
      await axios.post(`${API_BASE_URL}/favorites/add`, {
        user_id: userId,
        location_name: locationName,
      });
      setError('');
      alert('Location added to favorites!');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Delete a favorite location
  const deleteFavorite = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/favorites/delete/`, {
        data: {
          user_id: userId,
          location_name: locationName,
        },
      });
      setError('');
      alert('Location removed from favorites!');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  const fetchAllFavorites = async() => {
    try{
      await axios.get(`${API_BASE_URL}/favorites/get-all-favs/`, {
        data: {
          user_id: userId
        }
      });
      setError('');
      alert('All favorites fetched!');
    }  catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Weather App</h1>

      {!isLoggedIn ? (
        <div>
          <h2>User Authentication</h2>
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
          <button onClick={login}>Login</button>
          <button onClick={register}>Register</button>
        </div>
      ) : (
        <div>
          <h2>User Actions</h2>
          <label>User ID: </label>
          <input type="text" value={userId} readOnly />
          <br />
          <label>Location Name: </label>
          <input
            type="text"
            value={locationName}
            onChange={(e) => setLocationName(e.target.value)}
          />
          <br />
          <button onClick={fetchHourlyForecast}>Get Hourly Forecast</button>
          <button onClick={fetchDailyForecast}>Get Daily Forecast</button>
          <button onClick={addFavorite}>Add to Favorites</button>
          <button onClick={deleteFavorite}>Delete from Favorites</button>
          <button onClick={fetchFavoritesWeather}>Get Favorites Weather</button>
          <button onClick={fetchAllFavorites}>Get All Favorites</button>
        </div>
      )}

      {forecastData && (
        <div>
          <h2>Forecast Data</h2>
          <pre>{JSON.stringify(forecastData, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div style={{ color: 'red' }}>
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default App;
