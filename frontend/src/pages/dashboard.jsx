import { useEffect, useState } from "react";
import apiRequest from "../api";

export default function Dashboard({ userId }) {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    apiRequest(`/favorites/get-all-favs/?user_id=${userId}`)
      .then(data => setFavorites(data.favorite_locations))
      .catch(console.error);
  }, [userId]);

  return (
    <ul>
      {favorites.map(loc => (
        <li key={loc}>{loc}</li>
      ))}
    </ul>
  );
}
