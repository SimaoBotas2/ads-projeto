import type { Movie } from "../pages/browsePage";

export default function MovieCard({
  item,
  onClick,
}: {
  item: Movie;
  onClick?: (movie: Movie) => void;
}) {
  return (
    <div onClick={() => onClick?.(item)}>
      <div className="w-full max-h-[300px] aspect-2/3 bg-gray-700 overflow-hidden">
        <img
          src={item.poster_path}
          alt={item.name}
          className="w-full h-full object-cover"
        />
      </div>

      <div className="p-2">
        <h3 className="font-bold text-sm text-[#F5F5F5]">{item.name}</h3>
        <div className="flex items-center gap-2 text-xs mt-1">
          <span className="text-[#BBBBBB]">
            ⭐ {item.avg_rating?.toFixed(1) ?? "N/A"}
          </span>
          {item.count_rating > 0 && (
            <span className="text-[#888888]">({item.count_rating})</span>
          )}
        </div>
      </div>
    </div>
  );
}
