import { Navigate } from "react-router-dom";

import useAuth from "./utils/auth/useAuth";

export interface ProtectedRouteProps {
  component: React.FC;
}

const ProtectedRoute = ({ component: Component }: ProtectedRouteProps) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Component /> : <Navigate to="/" />;
};

export default ProtectedRoute;
