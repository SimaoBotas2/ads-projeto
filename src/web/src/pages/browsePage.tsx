import { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";
import apiRequest from "../lib/apiRequest";
import MovieModal from "../components/movieModal";
import AuthModal from "../components/modal";

export interface Directors {
  id: number;
  name: string;
}

export interface Genres {
  id: number;
  name: string;
}

export interface Movie {
  id: number;
  poster_path: string;
  description: string;
  launch_date: string;
  nationality: string;
  directors: Directors[];
  genres: Genres[];
  name: string;
  rating: string;
  avg_rating: number;
  count_rating: number;
  onClick?: (movie: Movie) => void;
}

export default function BrowsePage() {
  const [moviesSearched, setMoviesSearched] = useState<Movie[] | null>(null);
  const token = localStorage.getItem("token") || "";
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [currentRating, setCurrentRating] = useState<number | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  useEffect(() => {
    async function fetchMovies() {
      try {
        const response = await apiRequest.get(`/movies`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setMoviesSearched(response.data);
      } catch (error) {
        console.error("Error fetching initial movies:", error);
      }
    }
    fetchMovies();
  }, []);
  return (
    <div>
      <Navbar />

      <div>
        <SearchInput setMoviesSearched={setMoviesSearched} />

        <MovieModal
          movie={selectedMovie}
          currentRating={currentRating}
          onClose={() => setSelectedMovie(null)}
          onSubmitRating={async (rating) => {
            if (!selectedMovie) return;
            try {
              await apiRequest.post(
                `/ratings`,
                { evaluation: rating, movie_id: selectedMovie.id },
                {
                  params: {
                    user_id: JSON.parse(localStorage.getItem("user") || "{}")
                      .id,
                  },
                  headers: { Authorization: `Bearer ${token}` },
                }
              );
              setShowConfirmModal(true);
              setCurrentRating(rating);
            } catch (err) {
              console.error("Error submitting rating:", err);
              setShowConfirmModal(true);
            }
          }}
        />

        <AuthModal
          show={showConfirmModal}
          type="success"
          message="Rating saved successfully!"
          onClose={() => setShowConfirmModal(false)}
        />

        {moviesSearched && moviesSearched.length > 0 ? (
          <div className="py-6 px-14 min-w-full flex justify-start items-start gap-12 flex-wrap">
            {moviesSearched.map((movie, index) => (
              <div key={index} className=" min-w-[300px] pointer-events-auto">
                <MovieCard
                  item={movie}
                  onClick={() => setSelectedMovie(movie)}
                />
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
