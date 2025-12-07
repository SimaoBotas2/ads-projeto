import { ChevronUp, ChevronDown } from "lucide-react";
import type { RatedMovie } from "../pages/ratingsPage";

type SortKey = "title" | "rating";
type SortOrder = "asc" | "desc";

export default function MovieTable({
  movies,
  sortKey,
  sortOrder,
  onSort,
  onRatingChange,
  onRemove,
}: {
  movies: RatedMovie[];
  sortKey: SortKey;
  sortOrder: SortOrder;
  onSort: (key: SortKey) => void;
  onRatingChange: (ratingId: number, newRating: number) => void;
  onRemove: (id: number) => void;
}) {
  const renderSortIcon = (key: SortKey) => {
    if (sortKey !== key) return null;
    return sortOrder === "asc" ? (
      <ChevronUp className="inline ml-1 w-4 h-4" />
    ) : (
      <ChevronDown className="inline ml-1 w-4 h-4" />
    );
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="px-4 py-2 text-left">Poster</th>

            <th
              className="px-4 py-2 text-left cursor-pointer"
              onClick={() => onSort("title")}
            >
              Title {renderSortIcon("title")}
            </th>

            <th
              className="px-4 py-2 text-left cursor-pointer"
              onClick={() => onSort("rating")}
            >
              Rating {renderSortIcon("rating")}
            </th>

            <th className="px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>

        <tbody className="transition-all ease-in-out duration-500">
          {movies.map((movie) => (
            <tr
              key={movie.id}
              className="border-b border-gray-800 hover:bg-gray-900 transition duration-300"
            >
              <td className="px-4 py-2">
                <img
                  src={movie.movie.poster_path}
                  alt={movie.movie.name}
                  className="w-20 h-30 object-cover rounded"
                />
              </td>

              <td className="px-4 py-2">{movie.movie.name}</td>

              <td className="px-4 py-2">
                <select
                  value={movie.evaluation}
                  onChange={(e) =>
                    onRatingChange(movie.id, Number(e.target.value))
                  }
                  className="bg-gray-800/40 text-white px-1 py-1 rounded w-fit
                  transition ease-in-out duration-200 hover:bg-gray-800/70 cursor-pointer
                  focus:outline-none"
                >
                  <option value="0">No Rating</option>
                  <option value="1">⭐</option>
                  <option value="2">⭐⭐</option>
                  <option value="3">⭐⭐⭐</option>
                  <option value="4">⭐⭐⭐⭐</option>
                  <option value="5">⭐⭐⭐⭐⭐</option>
                </select>
              </td>

              <td className="px-4 py-2">
                <button
                  onClick={() => onRemove(movie.id)}
                  className="bg-red-600 px-3 py-1 rounded cursor-pointer hover:bg-red-800 transition"
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
