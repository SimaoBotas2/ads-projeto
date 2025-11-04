import logo from "../assets/logo.svg";
import { User, ArrowDownIcon } from "lucide-react";

export default function Navbar() {
  return (
    <header className="bg-[#1E1E1E] text-[#F5F5F5] p-4 flex justify-between items-center min-h-[64px] min-w-full">
      <div>
        <a href="/">
          <img src={logo} alt="Logo" className="w-12" />
        </a>
      </div>

      <div>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <a
                href="#Genre"
                className="text-[#F5F5F5] hover:text-[#03DAC6]
                  transition-colors duration-300 ease-out font-bold
                "
              >
                Genre <ArrowDownIcon className="inline h-4 w-4" />
              </a>
            </li>
            <li>
              <a
                href="#Browse"
                className="text-[#F5F5F5] hover:text-[#03DAC6]
                  transition-colors duration-300 ease-out font-bold
                "
              >
                Browse
              </a>
            </li>
            <li>
              <a
                href="#Wishlist"
                className="text-[#F5F5F5] hover:text-[#03DAC6]
                  transition-colors duration-300 ease-out font-bold
                "
              >
                Wishlist
              </a>
            </li>
            <li>
              <a
                href="#Ratings"
                className="text-[#F5F5F5] hover:text-[#03DAC6]
                  transition-colors duration-300 ease-out font-bold
                "
              >
                Ratings
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <div>
        <a href="">
          <User
            className="text-[#03DAC6] h-10 w-8 
              hover:text-[#00756ad2] transition-colors duration-300 ease-out
            "
          />
        </a>
      </div>
    </header>
  );
}
