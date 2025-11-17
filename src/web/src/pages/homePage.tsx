import { useEffect, useState } from "react";
import RecommendationsCarousel from "../components/carousel";
import Navbar from "../components/navbar";
import type { Movie } from "./browse";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";

export default function HomePage() {
  const genres = [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Romance",
    "Sci-Fi",
    "Fantasy",
    "Thriller",
  ];
  const [moviesSearched, setMoviesSearched] = useState<Movie[] | null>(null);
  const [selectedGenre, setSelectedGenre] = useState("Action");

  const moviesByGenre = (genre: string) =>
    Array.from({ length: 10 }, (_, i) => ({
      title: `${genre} Movie ${i + 1}`,
      rating: "⭐⭐⭐⭐☆",
    }));

  useEffect(() => {
    const fetchMovies = async () => {
      const movies = await fetch("http://localhost:5005/movies").then((res) =>
        res.json()
      );
      console.log(movies);
    };
    fetchMovies();
  }, []);

  return (
    <div>
      <Navbar />

      <SearchInput setMoviesSearched={setMoviesSearched} />
      {moviesSearched && moviesSearched.length > 0 ? (
        moviesSearched.map((movie, index) => (
          <div className="flex justify-center items-start w-fit">
            <div key={index} className="p-6">
              <MovieCard {...movie} />
            </div>
          </div>
        ))
      ) : (
        <div>
          <RecommendationsCarousel
            title="Recommended for you"
            items={Array.from({ length: 12 }, (_, i) => ({
              title: `Top Pick ${i + 1}`,
              rating: "⭐⭐⭐⭐⭐",
            }))}
          />

          <section className="p-6">
            <h2 className="text-xl font-bold mb-4">Top Movies by Genre</h2>
            <div className="flex flex-wrap gap-4">
              {genres.map((genre, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedGenre(genre)}
                  className={`cursor-pointer px-4 py-2 rounded-full transition-colors ${
                    selectedGenre === genre
                      ? "bg-[#03DAC6] text-[#121212] font-bold"
                      : "bg-[#1E1E1E] hover:bg-accent-purple"
                  } hover:bg-[#bb86fc8c]
            `}
                >
                  {genre}
                </button>
              ))}
            </div>
          </section>

          <RecommendationsCarousel
            key={selectedGenre}
            title={`${selectedGenre} Movies`}
            items={moviesByGenre(selectedGenre)}
          />
        </div>
      )}
    </div>
  );
}
