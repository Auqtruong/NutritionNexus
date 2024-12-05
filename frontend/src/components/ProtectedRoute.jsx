import { Navigate } from "react-router-dom"
import { isAuthenticated } from "../utils/auth";

//Check if user is authenticated; render children components or navigate user to login page
const ProtectedRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;