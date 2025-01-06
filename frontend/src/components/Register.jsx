import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
    //track registration form input values
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        confirmPassword: "",
    });

    const [error, setError]     = useState("");
    const [success, setSuccess] = useState(false);
    const navigate              = useNavigate();

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    }

    const handleSubmit = async(event) => {
        event.preventDefault();
        const { username, password, confirmPassword } = formData;

        //validate password confirmation
        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        try {
            //API request to register user
            const response = await fetch("/api/user/register/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) { //registration failed
                throw new Error("Registration failed. Please try again.");
            }

            setSuccess(true);
            setError("");
            setTimeout(() => navigate("/login"), 2500); //redirect user to login page after successful registration
        }
        catch (error) {
            setError(error.message);
        }
    };
    return (
        <div>
            <h2>Create Account</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Enter username"
                    aria-label="Username"
                    required
                />
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter password"
                    aria-label="Password"
                    required
                />
                <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Confirm password"
                    aria-label="Confirm password"
                    required
                />
                <button type="submit">
                    Sign Up
                </button>
            </form>
            {/* Success and error color highlighting for user; redirect them to login page after */}
            {error && <p style={{ color: "red" }}>{error}</p>}
            {success && <p style={{ color: "green" }}>Registration successful! Redirecting...</p>} 
        </div>
    );
};

export default Register;