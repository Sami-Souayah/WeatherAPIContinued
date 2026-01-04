import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
import Favorites from "./pages/favorites";

export default function App() {
  const [userId, setUserId] = useState(null);

  return (
    <Router>
      <Routes>
        {!userId ? (
          <Route path="*" element={<Login onLogin={setUserId} />} />
        ) : (
          <>
            <Route path="/favorites" element={<Favorites userId={userId} />} />
            <Route path="*" element={<Navigate to="/favorites" />} />
          </>
        )}
      </Routes>
    </Router>
  );
}