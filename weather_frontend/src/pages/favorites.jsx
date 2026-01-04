import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function Favorites({ userId }) {
  const [favorites, setFavorites] = useState([]);
  const [error, setError] = useState("");

  const loadFavorites = async () => {
    try {
      const res = await apiRequest(`/favorites/get-all-favs/?user_id=${userId}`);
      setFavorites(res.favorite_locations || []);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadFavorites();
  }, []);

  return (
    <div className="min-h-screen bg-sky-100 p-8">
      <h1 className="text-3xl font-semibold mb-6 text-sky-800">Your Favorite Locations</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {favorites.map((loc) => (
          <Card key={loc} className="hover:shadow-xl transition">
            <CardContent className="p-4">
              <h3 className="text-xl font-bold text-sky-700">{loc}</h3>
              <Button
                className="mt-3 bg-sky-500 hover:bg-sky-600"
                onClick={() => window.alert(`Fetching weather for ${loc}`)}
              >
                View Weather
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}