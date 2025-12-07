import type { Movie } from "../pages/browsePage";

export default function MovieCard({
  item,
  onClick,
}: {
  item: Movie;
  onClick?: (movie: Movie) => void;
}) {
  console.log("Rendering MovieCard for:", item);
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
        {/* <p className="text-[#BBBBBB] text-xs mt-1">Rating: {item.avg_rating}</p> */}
      </div>
    </div>
  );
}
