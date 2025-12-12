import { useState } from "react";
import apiRequest from "../lib/apiRequest";
import type { Movie } from "../pages/browsePage";

interface UseMovieRecommendationsProps {
  userId: number;
  token: string;
}

export function useMovieRecommendations({
  userId,
  token,
}: UseMovieRecommendationsProps) {
  const [moviesByGenre, setMoviesByGenre] = useState<Movie[]>([]);
  const [recommendationsByGenre, setRecommendationsByGenre] = useState<Movie[]>(
    []
  );
  const [recommendationsByDirector, setRecommendationsByDirector] = useState<
    Movie[]
  >([]);
  const [recommendationsByCast, setRecommendationsByCast] = useState<Movie[]>(
    []
  );

  const fetchMoviesByGenre = async (genreId: number): Promise<Movie[]> => {
    if (!userId || !genreId) return [];
    try {
      const response = await apiRequest.get(`movies/genre/${genreId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMoviesByGenre(response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching movies by genre:", error);
      return [];
    }
  };

  const fetchRecommendationsByGenre = async (): Promise<Movie[]> => {
    if (!userId) return [];
    try {
      const response = await apiRequest.get(`recommendations/genre`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${token}` },
      });
      setRecommendationsByGenre(response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching recommendations by genre:", error);
      return [];
    }
  };

  const fetchRecommendationsByDirector = async (): Promise<Movie[]> => {
    if (!userId) return [];
    try {
      const response = await apiRequest.get(`recommendations/director`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${token}` },
      });
      setRecommendationsByDirector(response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching recommendations by director:", error);
      return [];
    }
  };

  const fetchRecommendationsByCast = async (): Promise<Movie[]> => {
    if (!userId) return [];
    try {
      const response = await apiRequest.get(`recommendations/cast`, {
        params: { user_id: userId },
        headers: { Authorization: `Bearer ${token}` },
      });
      setRecommendationsByCast(response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching recommendations by cast:", error);
      return [];
    }
  };

  const fetchAllRecommendations = async (genreId?: number) => {
    await Promise.all([
      genreId ? fetchMoviesByGenre(genreId) : Promise.resolve(),
      fetchRecommendationsByGenre(),
      fetchRecommendationsByDirector(),
      fetchRecommendationsByCast(),
    ]);
  };

  const updateMovieInLists = (movieId: number, updates: Partial<Movie>) => {
    const updateFn = (movies: Movie[]) =>
      movies.map((m) => (m.id === movieId ? { ...m, ...updates } : m));

    setMoviesByGenre(updateFn);
    setRecommendationsByGenre(updateFn);
    setRecommendationsByDirector(updateFn);
    setRecommendationsByCast(updateFn);
  };

  return {
    moviesByGenre,
    recommendationsByGenre,
    recommendationsByDirector,
    recommendationsByCast,
    fetchMoviesByGenre,
    fetchAllRecommendations,
    updateMovieInLists,
  };
}
