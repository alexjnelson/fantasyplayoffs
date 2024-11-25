import { GoogleLogin } from "@react-oauth/google";
import { useState } from "react";

import useAuth from "../utils/auth/useAuth";

const HomePage = () => {
  const {
    handleGoogleLogin,
    googleLogin,
    handleDevLogin,
    handleDevCreateAccount,
  } = useAuth();
  const [email, setEmail] = useState<string>("");
  const [name, setName] = useState<string>("");

  return (
    <>
      <h1>Homepage boilerplate</h1>
      {
            googleLogin ? <GoogleLogin onSuccess={handleGoogleLogin} /> :
            <>
                <h1>Dev Login</h1>
                <h2>Email</h2>
                <input value={email} onChange={e => setEmail(e.target.value)} />
                <button onClick={() => handleDevLogin(email)} >Login</button>
                
                <h1>Dev Create Account</h1>
                <h2>Email</h2>
                <input value={email} onChange={e => setEmail(e.target.value)} />
                <h2>Name</h2>
                <input value={name} onChange={e => setName(e.target.value)} />
                <button onClick={() => handleDevCreateAccount(email, name)} >Create Account</button>
            </>
      }
    </>
  );
};

export default HomePage;
