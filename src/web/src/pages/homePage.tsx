import { useEffect, useState } from "react";
import RecommendationsCarousel from "../components/carousel";
import Navbar from "../components/navbar";
import SearchInput from "../components/searchInput";
import MovieCard from "../components/movieCard";
import type { Movie } from "./browsePage";
import MovieModal from "../components/movieModal";
import AuthModal from "../components/modal";
import { useGenres } from "../hooks/useGenres";
import { useMovieRecommendations } from "../hooks/useMovieRecommendations";
import { useMovieRating } from "../hooks/useMovieRating";

export default function HomePage() {
  const token = localStorage.getItem("token") || "";
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const [moviesSearched, setMoviesSearched] = useState<Movie[] | null>(null);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);

  const { genres, selectedGenre, setSelectedGenre } = useGenres({
    userId: user.id,
    token,
  });

  const {
    moviesByGenre,
    recommendationsByGenre,
    recommendationsByDirector,
    recommendationsByCast,
    fetchMoviesByGenre,
    fetchAllRecommendations,
    updateMovieInLists,
  } = useMovieRecommendations({
    userId: user.id,
    token,
  });

  const { currentRating, showConfirmModal, setShowConfirmModal, submitRating } =
    useMovieRating({
      movie: selectedMovie,
      userId: user.id,
      token,
      onRatingSubmitted: (updatedMovie) => {
        setSelectedMovie(updatedMovie);
        updateMovieInLists(updatedMovie.id, {
          avg_rating: updatedMovie.avg_rating,
          count_rating: updatedMovie.count_rating,
        });

        if (moviesSearched) {
          setMoviesSearched(
            (prev) =>
              prev?.map((m) =>
                m.id === updatedMovie.id
                  ? {
                      ...m,
                      avg_rating: updatedMovie.avg_rating,
                      count_rating: updatedMovie.count_rating,
                    }
                  : m
              ) || null
          );
        }

        if (selectedGenre?.id) {
          fetchAllRecommendations(selectedGenre.id);
        }
      },
    });

  useEffect(() => {
    if (selectedGenre?.id) {
      fetchAllRecommendations(selectedGenre.id);
    }
  }, [selectedGenre, fetchAllRecommendations]);

  const handleGenreChange = async (genreId: number) => {
    const genre = genres.find((g) => g.id === genreId);
    if (genre) {
      setSelectedGenre(genre);
      await fetchMoviesByGenre(genreId);
    }
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
        moviesSearched.map((movie, index) => (
          <div key={index} className="flex justify-center items-start w-fit">
            <div className="p-6">
              <MovieCard item={movie} onClick={() => setSelectedMovie(movie)} />
            </div>
          </div>
        ))
      ) : (
        <>
          {recommendationsByDirector.length > 0 && (
            <RecommendationsCarousel
              title="Recommended By Director"
              items={recommendationsByDirector.map((m) => ({
                ...m,
                onClick: () => setSelectedMovie(m),
              }))}
            />
          )}

          {recommendationsByCast.length > 0 && (
            <RecommendationsCarousel
              title="Recommended By Cast"
              items={recommendationsByCast.map((m) => ({
                ...m,
                onClick: () => setSelectedMovie(m),
              }))}
            />
          )}

          {recommendationsByGenre.length > 0 && (
            <RecommendationsCarousel
              key={`recommendations-${selectedGenre?.id}`}
              title="Recommended Movies by Genre"
              items={recommendationsByGenre.map((m) => ({
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
                  onClick={() => handleGenreChange(genre.id)}
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
