import { useState } from "react";
import RecommendationsCarousel from "../components/carousel";
import Navbar from "../components/navbar";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";

export interface Movie {
  title: string;
  rating: string;
}

export default function BrowsePage() {
  const [moviesSearched, setMoviesSearched] = useState<Movie[] | null>(null);
  console.log(moviesSearched);
  return (
    <div>
      <Navbar />

      <div>
        <SearchInput setMoviesSearched={setMoviesSearched} />

        {moviesSearched && moviesSearched.length > 0 ? (
          moviesSearched.map((movie, index) => (
            <div key={index} className="p-6">
              <MovieCard {...movie} />
            </div>
          ))
        ) : (
          <div className="p-4">
            <RecommendationsCarousel
              title="Top 10 recomentations for you"
              items={Array.from({ length: 12 }, (_, i) => ({
                title: `Top Pick ${i + 1}`,
                rating: "⭐⭐⭐⭐⭐",
              }))}
            />
          </div>
        )}
      </div>
    </div>
  );
}
