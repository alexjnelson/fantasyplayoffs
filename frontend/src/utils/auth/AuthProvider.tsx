import { useState, ReactNode, useMemo, useEffect } from "react";
import { CredentialResponse } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";

import AuthContext from "./AuthContext";
import {
  authenticate,
  devCreateAccount,
  devLogin,
} from "../../services/authService";
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
      !!(
        process.env.REACT_APP_ENVIRONMENT === "prod" &&
        process.env.REACT_APP_GOOGLE_CLIENT_ID
      ),
    []
  );

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setToken(token || undefined);
      setIsAuthenticated(true);
    }
  }, [setToken]);

  const handleLogin = (token: string) => {
    setToken(token);
    localStorage.setItem("token", token);
    setIsAuthenticated(true);

    navigate("/dashboard");
  };

  const handleGoogleLogin = (response: CredentialResponse | undefined) => {
    if (response && response.credential) {
      authenticate(axios, response.credential)
        .then(() => {
          handleLogin(response.credential!);
        })
        .catch(
          // TO DO: improve error handling
          () => alert("Login failed")
        );
    } else {
      // TO DO: improve error handling
      alert("Login failed");
    }
  };

  const handleDevLogin = (email: string) => {
    devLogin(axios, email)
      .then(() => {
        handleLogin(email);
      })
      .catch(
        // TO DO: improve error handling
        () => alert("Login failed")
      );
  };

  const handleDevCreateAccount = (email: string, name: string) => {
    devCreateAccount(axios, email, name)
      .then(() => {
        handleLogin(email);
      })
      .catch(
        // TO DO: improve error handling
        () => alert("Login failed")
      );
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(undefined);
    setIsAuthenticated(false);
    navigate("/");
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
