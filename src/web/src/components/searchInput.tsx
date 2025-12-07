import { Search } from "lucide-react";
import type { Movie } from "../pages/browsePage";
import type { Dispatch, SetStateAction } from "react";
import apiRequest from "../lib/apiRequest";
interface SearchInputProps {
  setMoviesSearched: Dispatch<SetStateAction<Movie[] | null>>;
}

export default function SearchInput(props: SearchInputProps) {
  const token = localStorage.getItem("token") || "";
  const { setMoviesSearched } = props;
  const debounceDelay = 300;

  async function handleSearch(query: string) {
    setTimeout(() => {
      performSearch(query);
    }, debounceDelay);
  }

  async function performSearch(query: string) {
    try {
      const response = await apiRequest.get(`/movies/search/?query=${query}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMoviesSearched(response.data);
    } catch (error) {
      console.error("Error searching movies:", error);
      setMoviesSearched([]);
    }
  }

  return (
    <section className="p-6 flex justify-center">
      <div className="w-full max-w-xl relative">
        <input
          type="text"
          placeholder="Search for movies..."
          onChange={async (e) => await handleSearch(e.target.value)}
          className="w-full bg-[#1E1E1E] text-[#F5F5F5] placeholder:text-[#BBBBBB] rounded-full py-3 px-4 pl-12 focus:outline-none focus:ring-2 focus:ring-[#03dac580] transition duration-200 ease-out"
        />
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-[#03dac580]" />
      </div>
    </section>
  );
}
