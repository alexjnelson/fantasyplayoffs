import useAuth from "../utils/auth/useAuth";

function Header() {
    const {isAuthenticated, handleLogout} = useAuth();

    return (
        <>
            {isAuthenticated ? 
                <button 
                    onClick={handleLogout}
                >Logout</button> 
                : null
            }
        </>
    );
}

export default Header;