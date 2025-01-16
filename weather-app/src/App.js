import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Register from './Register'; 
import axios from 'axios';
import UpdatePass from './UpdatePass'

const API_BASE_URL = 'http://127.0.0.1:5000';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState('');
  const [locationName, setLocationName] = useState('');
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [favoriteData, setFavoriteData] = useState(null);
  const [showFavorites, setShowFavorites] = useState(true);
  const [showForecast, setShowForecast] = useState(true);
  const [showPassword, setShowPassword] = useState(false)

  const navigate = useNavigate();  // Use useNavigate

  const toggleFavorites = () => setShowFavorites(!showFavorites);
  const toggleForecast = () => setShowForecast(!showForecast);
  const logout = () => {
    setUserId('');
    setIsLoggedIn(false);
    setLocationName('');
    setForecastData(null);  
    setFavoriteData(null);   
    setError('');
    setUsername('');
    setPassword(''); 
    alert('Logged out successfully!');
  };

  const clearall = () => {setLocationName('');setFavoriteData(null);setForecastData(null)}

  const fetchHourlyForecast = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/favorite/hourly/`,{ params: {location_name : locationName, user_id: userId}});
      setForecastData(response.data.hourly_forecast);
      setError('');
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  // Fetch daily forecast
  const fetchDailyForecast = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/favorite/daily/`, { params: {location_name : locationName, user_id: userId}});
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
      alert("Fetched weather for all favorite locations!")
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  };

  const fetchOneFavWeather = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/favorite/get-weather-for-favo/`, {
        params: { user_id: userId,location_name: locationName },
      });
      setForecastData(response.data.weather_loc);
      setError('');
      alert("Fetched weather for location!")
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
      const response = await axios.get(`${API_BASE_URL}/favorites/get-all-favs/`, {
        params: {
          user_id: userId
        }
      });
      setFavoriteData(response.data.favorite_locations);
      setError('');
    }  catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    }
  }

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
      setUsername(''); 
      setPassword(''); 
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred')
      setUsername(''); 
      setPassword(''); 
    }
  };

  const goToRegister = () => {
    navigate('/register');  
  };

  const goToUpdatePass = () => {
    navigate('/update-pass')
  };

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
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style = {{marginRight : '10px', marginBottom : '10px'}}
          />
          <button type="button"
            onMouseDown={() => setShowPassword(true)} // Show password when button is held
            onMouseUp={() => setShowPassword(false)} // Hide password when button is released
          onMouseLeave={() => setShowPassword(false)}> Show Password </button>
          <br />
          <button onClick={login}>Login</button>
          <button onClick={goToRegister}>Go to Register</button> {/* Button to navigate to registration */}
          <button onClick={goToUpdatePass}>Update Password</button>
        </div>
      ) : (
        <div>
          <h2>User Actions</h2>
          <label>User ID: </label>
          <label>{userId}</label>
          <br />
          <label>Location Name: </label>
          <input
            type="text"
            value={locationName}
            onChange={(e) => setLocationName(e.target.value)}
          />
            <button onClick={addFavorite}>Add to Favorites</button>
            <button onClick={deleteFavorite}>Delete from Favorites</button>
          <br />
          <button onClick={() => {alert('Fetching hourly forecast...');fetchHourlyForecast()}}>Get Hourly Forecast</button>
          <button onClick={() => {alert('Fetching daily forecast...');fetchDailyForecast()}}>Get Daily Forecast</button>
          <button onClick={() => {alert("Fetching weather for all favorites...");fetchFavoritesWeather();toggleFavorites()}}>Get Favorites Weather</button>
          <button onClick={() => {alert("Fetching all favorites...");fetchAllFavorites();toggleForecast()}}>Get All Favorites</button>
          <button onClick={() => {alert("Fetching the weather for location...");fetchOneFavWeather();toggleForecast()}}>Weather At Favorite</button>
          <button onClick={clearall}>Clear All</button>
          <button onClick={logout}>Log out</button>

        </div>
      )}
      {favoriteData && 
        <div>
          <h2> Favorites: </h2>
          <pre>{JSON.stringify(favoriteData, null,2)}</pre>
        </div>
      }
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

const AppWrapper = () => (
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/register" element={<Register />} />
      <Route path="/update-pass" element={<UpdatePass />} />
    </Routes>
  </Router>
);

export default AppWrapper;
