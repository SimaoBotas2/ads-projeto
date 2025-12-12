import { X, Star } from "lucide-react";
import { useState, useEffect } from "react";
import type { Movie } from "../pages/browsePage";

export default function MovieModal({
  movie,
  currentRating,
  onClose,
  onSubmitRating,
}: {
  movie: Movie | null;
  currentRating: number | null;
  onClose: () => void;
  onSubmitRating: (rating: number) => void;
}) {
  const [rating, setRating] = useState<number>(currentRating ?? 0);

  console.log("Current Rating:", movie);

  useEffect(() => {
    setRating(currentRating ?? 0);
  }, [currentRating]);

  if (!movie) return null;

  const handleSave = () => {
    onSubmitRating(rating);
    onClose();
  };

  console.log("Rendering MovieModal for movie:", movie);
  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex justify-center items-center z-50">
      <div className="bg-[#1E1E1E] rounded-2xl p-6 max-w-2xl w-full shadow-2xl border border-gray-700/40 overflow-y-auto max-h-[90vh]">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-white tracking-wide">
            {movie.name}
          </h2>
          <button onClick={onClose} className="hover:text-red-400 transition">
            <X size={26} />
          </button>
        </div>

        <div className="flex gap-6">
          <img
            src={movie.poster_path}
            className="w-48 h-auto rounded-lg shadow-lg object-cover"
          />

          <div className="flex-1 text-gray-200 space-y-3">
            <p className="text-gray-300 leading-relaxed">{movie.description}</p>

            <p>
              <span className="font-semibold text-white">Launch Date:</span>{" "}
              {movie.launch_date}
            </p>

            <p>
              <span className="font-semibold text-white">Nationality:</span>{" "}
              {movie.nationality}
            </p>

            <p>
              <span className="font-semibold text-white">Genres:</span>{" "}
              {movie.genres?.map((g) => g.name).join(", ")}
            </p>

            <p>
              <span className="font-semibold text-white">Directors:</span>{" "}
              {movie.directors?.map((d) => d.name).join(", ")}
            </p>

            <div className="flex items-center gap-2 mt-2">
              <span className="font-semibold text-white">Average Rating:</span>
              <div className="flex items-center gap-1">
                <Star className="text-yellow-400 fill-yellow-400" size={18} />
                <span>{movie.avg_rating ?? "N/A"}</span>
                <span className="text-gray-400 text-sm">
                  ({movie.count_rating} rating)
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <label className="block mb-2 text-lg font-semibold text-white">
            Your Rating:
          </label>
          <select
            className="w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 shadow-inner"
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
          >
            <option value={0}>No Rating</option>
            <option value={1}>⭐</option>
            <option value={2}>⭐⭐</option>
            <option value={3}>⭐⭐⭐</option>
            <option value={4}>⭐⭐⭐⭐</option>
            <option value={5}>⭐⭐⭐⭐⭐</option>
          </select>
        </div>

        <button
          onClick={handleSave}
          className="w-full mt-6 bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold tracking-wide shadow-lg transition"
        >
          Save Rating
        </button>
      </div>
    </div>
  );
}
