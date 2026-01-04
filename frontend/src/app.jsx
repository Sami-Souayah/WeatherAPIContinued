import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [userId, setUserId] = useState(null);

  if (!userId) {
    return <Login onLogin={setUserId} />;
  }

  return <Dashboard userId={userId} />;
}
