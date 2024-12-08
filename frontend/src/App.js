import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Logout from "./components/Logout";
import ProtectedRoute from "./components/ProtectedRoute";
import DailyIntake from "./components/DailyIntake";
import FoodDetail from "./components/FoodDetail";
import FoodList from "./components/FoodList";
import WeightTracker from "./components/WeightTracker";
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
                {/* Logout route */}
                <Route
                    path="/logout"
                    element={
                        <ProtectedRoute>
                            <Logout />
                        </ProtectedRoute>
                    }
                />
                {/* Daily Intake route */}
                <Route
                    path="/daily-intake"
                    element={
                        <ProtectedRoute>
                            <DailyIntake />
                        </ProtectedRoute>
                    }
                />
                {/* Food List route */}
                <Route
                    path="/food-list"
                    element={
                        <ProtectedRoute>
                            <FoodList />
                        </ProtectedRoute>
                    }
                />
                {/* Food Detail route */}
                <Route
                    path="/food/:foodId"
                    element={
                        <ProtectedRoute>
                            <FoodDetail />
                        </ProtectedRoute>
                    }
                />
                {/* Weight Tracker route */}
                <Route
                    path="/weight-tracker"
                    element={
                        <ProtectedRoute>
                            <WeightTracker />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;