import { useState, useEffect } from "react";
import apiRequest from "../lib/apiRequest";

export interface Genre {
  id: number;
  name: string;
  description: string;
}

interface UseGenresProps {
  userId: number;
  token: string;
}

export function useGenres({ userId, token }: UseGenresProps) {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<Genre | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return;

    const fetchGenres = async () => {
      try {
        setLoading(true);
        const response = await apiRequest.get(`genres`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setGenres(response.data);

        if (response.data.length > 0) {
          setSelectedGenre(response.data[0]);
        }
      } catch (error) {
        console.error("Error fetching genres:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGenres();
  }, [userId, token]);

  return {
    genres,
    selectedGenre,
    setSelectedGenre,
    loading,
  };
}
