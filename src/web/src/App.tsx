import { useState } from "react";
import RecommendationsCarousel from "./components/carousel";
import Navbar from "./components/navbar";
import { Search } from "lucide-react";

function App() {
  const genres = [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Romance",
    "Sci-Fi",
    "Fantasy",
    "Thriller",
  ];

  const [selectedGenre, setSelectedGenre] = useState("Action");

  const moviesByGenre = (genre: string) =>
    Array.from({ length: 10 }, (_, i) => ({
      title: `${genre} Movie ${i + 1}`,
      rating: "⭐⭐⭐⭐☆",
    }));

  return (
    <div className="bg-[#121212] min-h-screen min-w-full text-[#F5F5F5]">
      <Navbar />

      <section className="p-6 flex justify-center">
        <div className="w-full max-w-xl relative">
          <input
            type="text"
            placeholder="Search for movies..."
            className="w-full bg-[#1E1E1E] text-[#F5F5F5] placeholder:text-[#BBBBBB] rounded-full py-3 px-4 pl-12 focus:outline-none focus:ring-2 focus:ring-[#03dac580] transition duration-200 ease-out"
          />
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-[#03dac580]" />
        </div>
      </section>

      <RecommendationsCarousel
        title="Recommended for you"
        items={Array.from({ length: 12 }, (_, i) => ({
          title: `Top Pick ${i + 1}`,
          rating: "⭐⭐⭐⭐⭐",
        }))}
      />

      <section className="p-6">
        <h2 className="text-xl font-bold mb-4">Browse by Genre</h2>
        <div className="flex flex-wrap gap-4">
          {genres.map((genre, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedGenre(genre)}
              className={`cursor-pointer px-4 py-2 rounded-full transition-colors ${
                selectedGenre === genre
                  ? "bg-[#03DAC6] text-[#121212] font-bold"
                  : "bg-[#1E1E1E] hover:bg-accent-purple"
              } hover:bg-[#bb86fc8c]
              `}
            >
              {genre}
            </button>
          ))}
        </div>
      </section>

      <RecommendationsCarousel
        key={selectedGenre}
        title={`${selectedGenre} Movies`}
        items={moviesByGenre(selectedGenre)}
      />
    </div>
  );
}

export default App;
