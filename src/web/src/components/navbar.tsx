import { Film } from "lucide-react";
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
              to="/"
              className="text-[#F5F5F5] hover:text-[#03DAC6] transition-colors duration-300 ease-out font-bold"
            >
              Home
            </Link>
          </li>
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
              to="/ratings"
              className="text-[#F5F5F5] hover:text-[#03DAC6] transition-colors duration-300 ease-out font-bold"
            >
              Ratings
            </Link>
          </li>
        </ul>
      </nav>

      <div>
        <Link to="/auth">
          <button
            onClick={() => {
              localStorage.removeItem("currentUser");
            }}
            className="flex items-center space-x-2 bg-red-600 hover:bg-red-900 text-white font-bold py-2 px-4 rounded transition-colors duration-300 ease-out cursor-pointer"
          >
            Logout
          </button>
        </Link>
      </div>
    </header>
  );
}
