import { useState } from "react";
import Navbar from "../components/navbar";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";

export interface Movie {
  id: number;
  image: string;
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
          <div className="py-6 px-2 min-w-full flex justify-center items-start gap-12 flex-wrap">
            {moviesSearched.map((movie, index) => (
              <div key={index} className=" min-w-[300px]">
                <MovieCard {...movie} />
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4">
            <span>
              No movies found. Please try searching for something else.
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
