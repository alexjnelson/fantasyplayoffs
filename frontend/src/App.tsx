import "./App.css";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { useState } from "react";

import Layout from "./components/Layout";
import Dashboard from "./pages/dashboard";
import AuthProvider from "./utils/auth/AuthProvider";
import ProtectedRoute from "./ProtectedRoute";
import AxiosProvider from "./utils/axios/AxiosProvider";

import HomePage from "./pages/homePage";
import TestPage from "./pages/testPage";

interface PageViewProps {
  token: string | undefined;
  setToken: (token: string | undefined) => void;
}

function PageView({ token, setToken }: PageViewProps) {
  return (
    <Router>
      <AxiosProvider token={token}>
        <AuthProvider setToken={setToken}>
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route
                path="/dashboard"
                element={<ProtectedRoute component={Dashboard} />}
              />
              <Route
                path="/testpage"
                element={<ProtectedRoute component={TestPage} />}
              />
            </Routes>
          </Layout>
        </AuthProvider>
      </AxiosProvider>
    </Router>
  );
}

function App() {
  const [token, setToken] = useState<string | undefined>();

  if (
    process.env.REACT_APP_ENVIRONMENT === "prod" &&
    process.env.REACT_APP_GOOGLE_CLIENT_ID
  ) {
    return (
      <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
        <PageView token={token} setToken={setToken} />
      </GoogleOAuthProvider>
    );
  } else {
    return <PageView token={token} setToken={setToken} />;
  }
}

export default App;
