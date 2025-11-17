import { useState } from "react";
import Navbar from "../components/navbar";
import type { Movie } from "./browsePage";
import MovieTable from "../components/movieTable";

type SortKey = "title" | "rating";
type SortOrder = "asc" | "desc";

export default function WishlistPage() {
  const [movies, setMovies] = useState<Movie[]>([
    {
      id: 1,
      title: "The Matrix",
      image: "https://m.media-amazon.com/images/I/51EG732BV3L.jpg",
      rating: "2",
    },
    {
      id: 2,
      title: "Pulp Fiction",
      image: "https://m.media-amazon.com/images/I/71c05lTE03L._AC_SY679_.jpg",
      rating: "3",
    },
    {
      id: 3,
      title: "Interstellar",
      image: "https://m.media-amazon.com/images/I/91kFYg4fX3L._SL1500_.jpg",
      rating: "4",
    },
  ]);

  const [sortKey, setSortKey] = useState<SortKey>("title");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

  const handleRemove = (id: number) => {
    setMovies((prev) => prev.filter((movie) => movie.id !== id));
  };

  const handleRatingChange = (id: number, newRating: string) => {
    setMovies((prev) =>
      prev
        .map((movie) =>
          movie.id === id ? { ...movie, rating: newRating } : movie
        )
        .filter((movie) => movie.rating !== "0")
    );
  };

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  const sortedWishlist = [...movies].sort((a, b) => {
    if (sortKey === "title") {
      return sortOrder === "asc"
        ? a.title.localeCompare(b.title)
        : b.title.localeCompare(a.title);
    } else {
      return sortOrder === "asc"
        ? parseInt(a.rating) - parseInt(b.rating)
        : parseInt(b.rating) - parseInt(a.rating);
    }
  });

  return (
    <div className="min-h-screen bg-[#121212] text-white">
      <Navbar />

      <section className="p-6">
        <h1 className="text-2xl font-bold mb-6">Your Ratings List</h1>

        <MovieTable
          movies={sortedWishlist}
          sortKey={sortKey}
          sortOrder={sortOrder}
          onSort={handleSort}
          onRatingChange={handleRatingChange}
          onRemove={handleRemove}
        />
      </section>
    </div>
  );
}
