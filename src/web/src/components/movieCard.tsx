import type { Movie } from "../pages/browsePage";

export default function MovieCard(item: Movie) {
  return (
    <div className="bg-[#1E1E1E] max-w-[300px] rounded-lg overflow-hidden hover:shadow-xl transition">
      <div className="w-full max-h-[300px] aspect-2/3 bg-gray-700 overflow-hidden">
        <img
          src={item.image}
          alt={item.title}
          className="w-full h-full object-cover"
        />
      </div>

      <div className="p-2">
        <h3 className="font-bold text-sm text-[#F5F5F5]">{item.title}</h3>
        <p className="text-[#BBBBBB] text-xs mt-1">
          Rating: {item.rating || "⭐⭐⭐☆"}
        </p>
      </div>
    </div>
  );
}
