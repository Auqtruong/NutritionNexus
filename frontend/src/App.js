import { BrowserRouter as Router, Routes, Router, Navigate } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import DailyIntakePage from "./pages/DailyIntakePage";
import FoodListPage from "./pages/FoodListPage";
import FoodDetailPage from "./pages/FoodDetailPage";
import WeightTrackerPage from "./pages/WeightTrackerPage";
import UserProfilePage from "./pages/UserProfilePage";
import ProtectedRoute from "./components/ProtectedRoute";
import { isAuthenticated } from "./utils/auth";

function App() {
    return (
        <Router>
            <Routes>
                {/* Path for undefined routes */}
                <Route 
                    path="*" 
                    element={<div>Page Not Found</div>} 
                />

                {/* Redirect default route/landing page ("/") to login route */}
                <Route 
                    path="/" 
                    element={<Navigate to="/login" />} 
                />
                
                {/* Register route */}
                <Route 
                    path="/register" 
                    element={<RegisterPage />} 
                />

                {/* Login route; route to daily intake if already logged in */}
                <Route
                    path="/login"
                    element={
                        isAuthenticated() ? (<Navigate to="/daily-intake" />) : (<LoginPage />)
                    }
                />

                {/* Daily Intake route */}
                <Route
                    path="/daily-intake"
                    element={
                        <ProtectedRoute>
                            <DailyIntakePage />
                        </ProtectedRoute>
                    }
                />

                {/* Food List route */}
                <Route
                    path="/food-list"
                    element={
                        <ProtectedRoute>
                            <FoodListPage />
                        </ProtectedRoute>
                    }
                />

                {/* Food Detail route */}
                <Route
                    path="/food/:foodId"
                    element={
                        <ProtectedRoute>
                            <FoodDetailPage />
                        </ProtectedRoute>
                    }
                />

                {/* Weight Tracker route */}
                <Route
                    path="/weight-tracker"
                    element={
                        <ProtectedRoute>
                            <WeightTrackerPage />
                        </ProtectedRoute>
                    }
                />

                {/* User Profile route */}
                <Route
                    path="/user-profile"
                    element={
                        <ProtectedRoute>
                            <UserProfilePage />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;