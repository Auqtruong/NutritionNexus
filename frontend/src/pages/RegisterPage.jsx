import { Link } from "react-router-dom";
import Register from "../components/Register";

const RegisterPage = () => {
    return (
        <div className="register-page">
            <h1>Sign Up</h1>
            <Register />
            <p>
                {/* navigation to Login page for existing users */}
                Already have an account?{" "}
                <Link to="/login" className="login-link">
                    Sign In
                </Link>
            </p>
        </div>
    );
};

export default RegisterPage;
