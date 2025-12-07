import { useEffect, useState } from "react";
import { AuthContext } from "./authContext";

export const AuthContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [currentUser, setCurrentUser] = useState(
    JSON.parse(localStorage.getItem("user") as string) || null
  );
  const [currentToken, setCurrentToken] = useState(
    localStorage.getItem("token") || ""
  );

  const updateUser = (user: unknown) => {
    setCurrentUser(user);
  };

  const updateToken = (token: unknown) => {
    if (typeof token === "string") {
      setCurrentToken(token);
    }
  };

  useEffect(() => {
    localStorage.setItem("user", JSON.stringify(currentUser));
    localStorage.setItem("token", currentToken);
  }, [currentUser, currentToken]);

  return (
    <AuthContext.Provider
      value={{ currentUser, currentToken, updateUser, updateToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
