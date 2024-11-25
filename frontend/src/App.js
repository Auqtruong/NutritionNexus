import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Logout from "./components/Logout";
import ProtectedRoute from "./components/ProtectedRoute";
import DailyIntake from "./components/DailyIntake"; //TO DO
import FetchDataFromApi from "./components/FetchDataFromApi"; //TO DO
import { isAuthenticated } from "./utils/auth";

function App() {
    return (
        <Router>
            <Routes>
                {/* Path for undefined routes */}
                <Route path="*" element={<div>Page Not Found</div>} />
                {/* Login route; route to daily intake if already logged in */}
                <Route
                    path="/login"
                    element={
                        isAuthenticated() ? (<Navigate to="/daily-intake" />) : (<Login />)
                    }
                />
                <Route
                    path="/logout"
                    element={
                        <ProtectedRoute>
                            <Logout />
                        </ProtectedRoute>
                    } />
                <Route
                    path="/daily-intake"
                    element={
                        <ProtectedRoute>
                            <DailyIntake />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;