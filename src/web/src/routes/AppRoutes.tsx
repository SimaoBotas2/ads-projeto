import { Routes, Route, Navigate } from "react-router-dom";
import HomePage from "../pages/homePage";
import AuthPage from "../pages/authPage";
import BrowsePage from "../pages/browsePage";
import RatingsPage from "../pages/ratingsPage";
import { useContext, type JSX } from "react";
import { AuthContext } from "../context/authContext";

function RequireAuth({ children }: { children: JSX.Element }) {
  const { currentUser } = useContext(AuthContext) as {
    currentUser: string | null;
  };
  return !currentUser ? <Navigate to="/auth" /> : children;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />

      <Route
        path="/home"
        element={
          <RequireAuth>
            <HomePage />
          </RequireAuth>
        }
      />
      <Route
        path="/ratings"
        element={
          <RequireAuth>
            <RatingsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/browse"
        element={
          <RequireAuth>
            <BrowsePage />
          </RequireAuth>
        }
      />

      <Route path="*" element={<Navigate to="/home" />} />
    </Routes>
  );
}
