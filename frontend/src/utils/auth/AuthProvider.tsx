import { useState, ReactNode, useMemo } from "react";
import { CredentialResponse } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";

import AuthContext from "./AuthContext";
import { authenticate } from "../../services/authService";
import useAxios from "../axios/useAxios";

interface AuthProviderProps {
  children: ReactNode;
  setToken: (token: string | undefined) => void;
}

const AuthProvider = ({
  setToken,
  children,
}: AuthProviderProps): JSX.Element => {
  const navigate = useNavigate();
  const { axios } = useAxios();

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const googleLogin = useMemo(
    () =>
      !!(process.env.REACT_APP_ENVIRONMENT === "prod" &&
      process.env.REACT_APP_GOOGLE_CLIENT_ID),
    []
  );

  const handleGoogleLogin = (response: CredentialResponse | undefined) => {
    if (response && response.credential) {
      authenticate(axios, response.credential);

      setToken(response.credential);
      localStorage.setItem("token", response.credential);
      setIsAuthenticated(true);

      navigate("/view-leagues");
    } else {
      // TO DO: improve error handling
      alert("Login failed");
    }
  };

  const handleDevLogin = (email: string) => {
    // TO DO: send to auth in backend
  };

  const handleDevCreateAccount = (email: string, name: string) => {
    // TO DO: send to auth in backend
  };

  const handleLogout = () => {
    setToken(undefined);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        googleLogin,
        handleGoogleLogin,
        handleDevLogin,
        handleDevCreateAccount,
        handleLogout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
