import { useState } from "react";
import apiRequest from "../api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const data = await apiRequest("/user/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      onLogin(data.user_id);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <input value={username} onChange={e => setUsername(e.target.value)} />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button>Login</button>
      {error && <p>{error}</p>}
    </form>
  );
}
