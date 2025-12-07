import { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import type { Movie } from "./browsePage";
import MovieTable from "../components/movieTable";
import apiRequest from "../lib/apiRequest";

type SortKey = "title" | "rating";
type SortOrder = "asc" | "desc";

export interface RatedMovie extends Movie {
  evaluation: number;
  movie: Movie;
}

export default function RatingsPage() {
  const [movies, setMovies] = useState<RatedMovie[]>([]);
  const [sortKey, setSortKey] = useState<SortKey>("title");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token") || "";

  const loadRatings = async () => {
    if (!user || !user.id) return;

    try {
      const response = await apiRequest.get(`/ratings/user/${user.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMovies(response.data);
    } catch (error) {
      console.error("Error fetching ratings:", error);
    }
  };

  const handleRemove = async (ratingId: number) => {
    try {
      await apiRequest.delete(`/ratings`, {
        params: { user_id: user.id, rating_id: ratingId },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      await loadRatings();
    } catch (error) {
      console.error("Error removing rating:", error);
    }
  };

  const handleUpdateRating = async (ratingId: number, newRating: number) => {
    try {
      if (newRating === 0) {
        handleRemove(ratingId);
        return;
      }

      await apiRequest.put(
        `/ratings`,
        { evaluation: newRating },
        {
          params: { user_id: user.id, rating_id: ratingId },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      await loadRatings();
    } catch (error) {
      console.error("Error updating rating:", error);
    }
  };

  const sortedWishlist = [...movies].sort((a, b) => {
    if (sortKey === "title") {
      return sortOrder === "asc"
        ? a.movie.name.localeCompare(b.movie.name)
        : b.movie.name.localeCompare(a.movie.name);
    }

    return sortOrder === "asc"
      ? a.evaluation - b.evaluation
      : b.evaluation - a.evaluation;
  });

  useEffect(() => {
    loadRatings();
  }, [user]);

  return (
    <div className="min-h-screen bg-[#121212] text-white">
      <Navbar />

      <section className="p-6">
        <h1 className="text-2xl font-bold mb-6">Your Ratings List</h1>

        <MovieTable
          movies={sortedWishlist}
          sortKey={sortKey}
          sortOrder={sortOrder}
          onSort={(key) => {
            setSortKey(key);
            setSortOrder((prevOrder) => (prevOrder === "asc" ? "desc" : "asc"));
          }}
          onRatingChange={handleUpdateRating}
          onRemove={handleRemove}
        />
      </section>
    </div>
  );
}
