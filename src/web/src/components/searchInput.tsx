import { Search } from "lucide-react";
import type { Movie } from "../pages/browsePage";
import type { Dispatch, SetStateAction } from "react";
interface SearchInputProps {
  setMoviesSearched: Dispatch<SetStateAction<Movie[] | null>>;
}

const mockMovies = Array.from({ length: 10 }, (_, i) => ({
  id: i + 1,
  image: `https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/960w/products/89058/93685/Joker-2019-Final-Style-steps-Poster-buy-original-movie-posters-at-starstills__62518.1669120603.jpg?c=2`,
  title: `Movie Title ${i + 1}`,
  rating: "⭐⭐⭐⭐☆",
}));

export default function SearchInput(props: SearchInputProps) {
  const { setMoviesSearched } = props;
  const debounceDelay = 300;

  function handleSearch(query: string) {
    setTimeout(() => {
      performSearch(query);
    }, debounceDelay);
  }

  function performSearch(query: string) {
    if (query.trim() === "") {
      setMoviesSearched(null);
    } else {
      const filteredMovies = mockMovies.filter((movie) =>
        movie.title.toLowerCase().includes(query.toLowerCase())
      );
      setMoviesSearched(filteredMovies);
      console.log(filteredMovies);
    }
  }
  //TODO: Verify with AI why does it search five times instead of once

  return (
    <section className="p-6 flex justify-center">
      <div className="w-full max-w-xl relative">
        <input
          type="text"
          placeholder="Search for movies..."
          onChange={(e) => handleSearch(e.target.value)}
          className="w-full bg-[#1E1E1E] text-[#F5F5F5] placeholder:text-[#BBBBBB] rounded-full py-3 px-4 pl-12 focus:outline-none focus:ring-2 focus:ring-[#03dac580] transition duration-200 ease-out"
        />
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-[#03dac580]" />
      </div>
    </section>
  );
}
