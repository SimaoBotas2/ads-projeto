import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/homePage";
import AuthPage from "../pages/authPage";
import BrowsePage from "../pages/browse";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/wishlist" element={<div>Wishlist Page</div>} />
      <Route path="/ratings" element={<div>Ratings Page</div>} />
      <Route path="/browse" element={<BrowsePage />} />
    </Routes>
  );
}
