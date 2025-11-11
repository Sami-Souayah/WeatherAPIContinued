import { useState } from "react";
import { apiRequest } from "../api/client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigation = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await apiRequest("/user/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      onLogin(res.user_id);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreateUser = () => {
    navigation("/createuser");
  }

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-br from-blue-100 to-blue-300">
      <Card className="w-96 shadow-lg rounded-2xl">
        <CardContent className="p-6">
          <h2 className="text-2xl font-semibold text-center mb-4">Login</h2>
          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button type="submit" className="w-full bg-blue-500 hover:bg-blue-600">
              Login
            </Button>
            <Button type="button" onClick={handleCreateUser} className="w-full bg-blue-500 hover:bg-blue-600"> Create User </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}


