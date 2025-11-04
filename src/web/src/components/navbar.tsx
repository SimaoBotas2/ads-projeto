import { User, Film } from "lucide-react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="bg-[#1E1E1E] text-[#F5F5F5] p-4 flex justify-between items-center min-h-16 min-w-full">
      <div>
        <Link to="/">
          <Film className="text-[#03DAC6] h-10 w-10" />
        </Link>
      </div>

      <nav>
        <ul className="flex space-x-6">
          <li>
            <Link
              to="/browse"
              className="text-[#F5F5F5] hover:text-[#03DAC6] transition-colors duration-300 ease-out font-bold"
            >
              Browse
            </Link>
          </li>
          <li>
            <Link
              to="/wishlist"
              className="text-[#F5F5F5] hover:text-[#03DAC6] transition-colors duration-300 ease-out font-bold"
            >
              Wishlist
            </Link>
          </li>
          <li>
            <Link
              to="/ratings"
              className="text-[#F5F5F5] hover:text-[#03DAC6] transition-colors duration-300 ease-out font-bold"
            >
              Ratings
            </Link>
          </li>
        </ul>
      </nav>

      <div>
        <Link to="/profile">
          <User className="text-[#03DAC6] h-10 w-8 hover:text-[#00756ad2] transition-colors duration-300 ease-out" />
        </Link>
      </div>
    </header>
  );
}
