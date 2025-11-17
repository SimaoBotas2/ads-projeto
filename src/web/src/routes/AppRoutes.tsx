import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/homePage";
import AuthPage from "../pages/authPage";
import BrowsePage from "../pages/browsePage";
import WishlistPage from "../pages/wishlistPage";
import RatingsPage from "../pages/ratingsPage";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/wishlist" element={<WishlistPage />} />
      <Route path="/ratings" element={<RatingsPage />} />
      <Route path="/browse" element={<BrowsePage />} />
    </Routes>
  );
}
