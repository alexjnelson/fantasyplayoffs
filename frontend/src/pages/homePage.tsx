import { GoogleLogin } from "@react-oauth/google";
import { useEffect, useState } from "react";

import useAuth from "../utils/auth/useAuth";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const {
    isAuthenticated,
    handleGoogleLogin,
    googleLogin,
    handleDevLogin,
    handleDevCreateAccount,
  } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState<string>("");
  const [name, setName] = useState<string>("");

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  return (
    <>
      <h1>Homepage boilerplate</h1>
      {googleLogin ? (
        <GoogleLogin onSuccess={handleGoogleLogin} />
      ) : (
        <>
          <h1>Dev Login</h1>
          <h2>Email</h2>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
          <button onClick={() => handleDevLogin(email)}>Login</button>

          <h1>Dev Create Account</h1>
          <h2>Email</h2>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
          <h2>Name</h2>
          <input value={name} onChange={(e) => setName(e.target.value)} />
          <button onClick={() => handleDevCreateAccount(email, name)}>
            Create Account
          </button>
        </>
      )}
    </>
  );
};

export default HomePage;
