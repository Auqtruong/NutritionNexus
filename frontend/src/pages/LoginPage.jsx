import { Link } from "react-router-dom";
import Login from "../components/Login";

const LoginPage = () => {
    return (
        <div className="login-page">
            <h1>Login</h1>
            <Login />
            <p>
                {/* allow users to register if they don't have an existing account */}
                Don't have an account?{" "}
                <Link to="/register" className="register-link">
                    Register
                </Link>
            </p>
        </div>
    );
};

export default LoginPage;
