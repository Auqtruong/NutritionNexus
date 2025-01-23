import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import DailyIntakePage from "./pages/DailyIntakePage";
import FoodListPage from "./pages/FoodListPage";
import FoodDetailPage from "./pages/FoodDetailPage";
import WeightTrackerPage from "./pages/WeightTrackerPage";
import UserProfilePage from "./pages/UserProfilePage";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardPage from "./pages/DashboardPage"
import Navbar from "./components/Navbar";
import { isAuthenticated } from "./utils/auth";

function App() {
    const [userData, setUserData] = useState(null);

    //Grab user profile data
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch("/api/user/profile/");
                if (!response.ok) { //unsuccessful fetch
                    throw new Error("Failed to fetch user data");
                }
                const data = await response.json();
                setUserData(data);
            }
            catch (error) {
                console.error("Error fetching user data:", error);
            }
        };
        fetchUserData();
    }, []);

    //Group routes/pages that use Navbar together
    const ProtectedLayout = ({ children }) => (
        <>
            <Navbar userData={userData} />
            {children}
        </>
    );

    return (
        <Router>
            <Routes>
                {/* Routes without Navbar */}
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route
                    path="/login"
                    element={isAuthenticated() ? (<Navigate to="/daily-intake" />) : (<LoginPage />)}
                />
                <Route path="*" element={<div>Page Not Found</div>} />

                {/* Routes with Navbar */}
                <Route
                    path="/food-list"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <FoodListPage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/daily-intake"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <DailyIntakePage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/food/:foodId"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <FoodDetailPage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/weight-tracker"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <WeightTrackerPage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/user-profile"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <UserProfilePage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <ProtectedLayout>
                                <DashboardPage />
                            </ProtectedLayout>
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;