import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";

import useAuth from "./utils/auth/useAuth";

export interface ProtectedRouteProps {
  component: React.FC;
}

const ProtectedRoute = ({ component: Component }: ProtectedRouteProps) => {
  const { isAuthenticated } = useAuth();
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    setIsInitialized(true);
  }, []);

  return isAuthenticated ? (
    <Component />
  ) : isInitialized ? (
    <Navigate to="/" />
  ) : null;
};

export default ProtectedRoute;
