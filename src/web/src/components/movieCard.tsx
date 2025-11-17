import type { Movie } from "../pages/browse";

export default function MovieCard(item: Movie) {
  return (
    <div className="bg-[#1E1E1E] max-w-[400px] rounded-lg overflow-hidden hover:shadow-xl transition">
      <div className="h-64 bg-gray-700"></div>
      <div className="p-2">
        <h3 className="font-bold text-sm text-[#F5F5F5]">{item.title}</h3>
        <p className="text-[#BBBBBB] text-xs mt-1">
          Rating: {item.rating || "⭐⭐⭐☆"}
        </p>
      </div>
    </div>
  );
}
