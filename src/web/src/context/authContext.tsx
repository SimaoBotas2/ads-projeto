import { createContext } from "react";

export const AuthContext = createContext<{
  currentUser: unknown;
  currentToken: unknown;
  updateUser: (user: unknown) => void;
  updateToken: (token: unknown) => void;
}>({
  currentUser: null,
  currentToken: null,
  updateUser: () => {},
  updateToken: () => {},
});
