import { createContext } from "react";
import { CredentialResponse } from "@react-oauth/google";

export interface AuthContextValue {
  isAuthenticated: boolean;
  googleLogin: boolean;
  handleGoogleLogin: (response: CredentialResponse | undefined) => void;
  handleDevLogin: (email: string) => void;
  handleDevCreateAccount: (email: string, name: string) => void;
  handleLogout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export default AuthContext;
