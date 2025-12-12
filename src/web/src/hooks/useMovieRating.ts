import { useState, useEffect } from "react";
import apiRequest from "../lib/apiRequest";
import type { Movie } from "../pages/browsePage";

interface UseMovieRatingProps {
  movie: Movie | null;
  userId: number;
  token: string;
  onRatingSubmitted?: (updatedMovie: Movie) => void;
}

export function useMovieRating({
  movie,
  userId,
  token,
  onRatingSubmitted,
}: UseMovieRatingProps) {
  const [currentRating, setCurrentRating] = useState<number | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  useEffect(() => {
    if (!movie || !userId) {
      setCurrentRating(null);
      return;
    }

    const fetchRating = async () => {
      try {
        const response = await apiRequest.get(`/ratings/${movie.id}`, {
          params: { user_id: userId },
          headers: { Authorization: `Bearer ${token}` },
        });
        setCurrentRating(response.data?.evaluation || 0);
      } catch (err) {
        console.error("Error loading user rating:", err);
        setCurrentRating(null);
      }
    };

    fetchRating();
  }, [movie, userId, token]);

  const submitRating = async (evaluation: number) => {
    if (!movie || !userId) return;

    try {
      await apiRequest.post(
        `/ratings`,
        { evaluation, movie_id: movie.id },
        {
          params: { user_id: userId },
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setCurrentRating(evaluation);
      setShowConfirmModal(true);

      const updatedMovieResponse = await apiRequest.get(`/movies/${movie.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const updatedMovie = {
        ...movie,
        avg_rating: updatedMovieResponse.data.avg_rating,
        count_rating: updatedMovieResponse.data.count_rating,
      };

      onRatingSubmitted?.(updatedMovie);
    } catch (err) {
      console.error("Error submitting rating:", err);
      setShowConfirmModal(true);
    }
  };

  return {
    currentRating,
    showConfirmModal,
    setShowConfirmModal,
    submitRating,
  };
}
