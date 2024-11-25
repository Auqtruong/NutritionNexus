import React from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../utils/auth.js"

const Logout = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        logout(); //call logout function from auth.js
        navigate("/login"); //redirect user to login page after logging out
    };

    return (
        <button onClick={handleLogout}>Logout</button>
    );
};