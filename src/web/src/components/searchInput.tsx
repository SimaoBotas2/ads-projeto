import { Search } from "lucide-react";

export default function SearchInput() {
  return (
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
  );
}
