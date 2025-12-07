import { useEffect, useState } from "react";
import RecommendationsCarousel from "../components/carousel";
import Navbar from "../components/navbar";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";
import apiRequest from "../lib/apiRequest";
import type { Movie } from "./browsePage";
import MovieModal from "../components/movieModal";
import AuthModal from "../components/modal";

interface Genre {
  id: number;
  name: string;
  description: string;
}

export default function HomePage() {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [moviesSearched, setMoviesSearched] = useState<Movie[] | null>(null);
  const [selectedGenre, setSelectedGenre] = useState<Genre | null>(null);
  const [moviesByGenre, setMoviesByGenre] = useState<Movie[]>([]);
  const [moviesRecommendationsForGenre, setMoviesRecommendationsForGenre] =
    useState<Movie[]>([]);
  const [currentRating, setCurrentRating] = useState<number | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const token = localStorage.getItem("token") || "";

  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);

  useEffect(() => {
    if (!user || !user.id) return;

    const fetchGenres = async () => {
      try {
        const genres = await apiRequest.get(`genres`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setGenres(genres.data);
      } catch (error) {
        console.error("Error fetching ratings:", error);
      }
    };

    fetchGenres();
  }, []);

  useEffect(() => {
    if (genres.length > 0) {
      setSelectedGenre(genres[0]);
      getMoviesRecommendationsForGenre(genres[0].id);
    }
  }, [genres]);

  async function getMoviesRecommendationsForGenre(
    genreId: number
  ): Promise<Movie[]> {
    if (!user || !user.id || !genreId) return [];
    try {
      const movieByGenre = await apiRequest.get(`movies/genre/${genreId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const recommendations = await apiRequest.get(`recommendations/genre`, {
        params: { user_id: user.id},
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMoviesByGenre(movieByGenre.data);
      setMoviesRecommendationsForGenre(recommendations.data);
      return recommendations.data;
    } catch (error) {
      console.error("Error fetching movies for genre:", error);
      return [];
    }
  }

  useEffect(() => {
    if (!selectedMovie || !user?.id) return;

    const fetchRating = async () => {
      try {
        const res = await apiRequest.get(`/ratings/${selectedMovie.id}`, {
          params: { user_id: user.id },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setCurrentRating(res.data?.evaluation || 0);
      } catch (err) {
        console.error("Error loading user rating:", err);
        setCurrentRating(null);
      }
    };

    fetchRating();
  }, [selectedMovie]);

  async function submitRating(evaluation: number) {
    if (!selectedMovie || !user?.id) return;

    try {
      await apiRequest.post(
        `/ratings`,
        { evaluation, movie_id: selectedMovie.id },
        {
          params: { user_id: user.id },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setShowConfirmModal(true);
      setCurrentRating(evaluation);
      refreshRecommendations();
    } catch (err) {
      console.error("Error submitting rating:", err);
      setShowConfirmModal(true);
    }
  }

  const refreshRecommendations = async () => {
    if (!selectedGenre?.id) return;
    await getMoviesRecommendationsForGenre(selectedGenre.id);
  };

  return (
    <div>
      <Navbar />
      <SearchInput setMoviesSearched={setMoviesSearched} />

      <MovieModal
        movie={selectedMovie}
        currentRating={currentRating}
        onClose={() => setSelectedMovie(null)}
        onSubmitRating={submitRating}
      />

      <AuthModal
        show={showConfirmModal}
        type="success"
        message="Rating saved successfully!"
        onClose={() => setShowConfirmModal(false)}
      />

      {moviesSearched ? (
        moviesSearched.map((movie) => (
          <div className="flex justify-center items-start w-fit">
            <div className="p-6">
              <MovieCard item={movie} onClick={() => setSelectedMovie(movie)} />
            </div>
          </div>
        ))
      ) : (
        <>
          <RecommendationsCarousel
            title="Recommended for you"
            items={moviesByGenre.map((m) => ({
              ...m,
              onClick: () => setSelectedMovie(m),
            }))}
          />

          {moviesRecommendationsForGenre.length > 0 && (
            <RecommendationsCarousel
              key={`recommendations-${selectedGenre?.id}`}
              title={`Recommended Movies by Genre`}
              items={moviesRecommendationsForGenre.map((m) => ({
                ...m,
                onClick: () => setSelectedMovie(m),
              }))}
            />
          )}

          <section className="p-6">
            <h2 className="text-xl font-bold mb-4">Top Movies by Genre</h2>
            <div className="flex flex-wrap gap-4">
              {genres.map((genre) => (
                <button
                  key={genre.id}
                  onClick={() => {
                    setSelectedGenre(genre);
                    getMoviesRecommendationsForGenre(genre.id);
                  }}
                  className={`cursor-pointer px-4 py-2 rounded-full transition-colors ${
                    selectedGenre?.id === genre.id
                      ? "bg-[#03DAC6] text-[#121212] font-bold"
                      : "bg-[#1E1E1E] hover:bg-accent-purple"
                  } hover:bg-[#bb86fc8c]`}
                >
                  {genre.name}
                </button>
              ))}
            </div>
          </section>

          <RecommendationsCarousel
            key={selectedGenre?.id}
            title={`${selectedGenre?.name} Movies`}
            items={moviesByGenre.map((m) => ({
              ...m,
              onClick: () => setSelectedMovie(m),
            }))}
          />
        </>
      )}
    </div>
  );
}
