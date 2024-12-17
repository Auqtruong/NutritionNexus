import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../utils/auth.js"

const Login = () => {
    //track input values for login form
    const [credentials, setCredentials] = useState({ username: "", password: "" });
    const [error, setError]             = useState("");
    const navigate                      = useNavigate();

    const handleChange = (event) => {
        const { name, value } = event.target;
        setCredentials({ ...credentials, [name]: value })
    };

    const handleSubmit = async (event) => {
        event.preventDefault(); //prevent default submission behavior
        try {
            await login(credentials); //call login function from auth.js
            navigate("/daily-intake"); //Redirect to User's Daily Intake page
        }
        catch (err) {
            setError("Invalid credentials. Please try again.");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>  
                <input
                    type="text"
                    name="username"
                    value={credentials.username}
                    onChange={handleChange}
                    placeholder="Enter username"
                    required
                />
                <input
                    type="password" //obscure text with asterisks "*"
                    name="password"
                    value={credentials.password}
                    onChange={handleChange}
                    placeholder="Enter password"
                    required
                />
                <button type="submit">Login</button>
            </form>
            {error && <p>{error}</p>}  {/* display the error if there is one when login unsuccessful*/}
        </div>
    );
};

export default Login;