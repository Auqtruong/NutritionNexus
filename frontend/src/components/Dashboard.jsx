import FetchDataFromApi from "./FetchDataFromApi";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const navigate = useNavigate();

    //render user's daily macros data
    const renderMacros = (data) => (
        <div className="card" onClick={() => navigate("/daily-intake")}>
            <h3>Today's Macros</h3>
            <p>Calories: {data.total_cals} kcal</p>
            <p>Carbohydrates: {data.total_carbs} g</p>
            <p>Protein: {data.total_protein} g</p>
            <p>Fats: {data.total_fat} g</p>
        </div>
    );

    //render user's most recent weight data
    const renderWeight = (data) => (
        <div className="card" onClick={() => navigate("/weight-tracker")}>
            <h3>Last Recorded Weight</h3>
            <p>
                Weight: {data.last_rec_weight !== null ? `${data.last_rec_weight} lbs` : "No data available"}
            </p>
            <p>
                Date: {data.last_weight_date !== null ? data.last_weight_date : "No data available"}
            </p>
        </div>
    );

    //render food list card
    const renderFoodList = () => (
        <div className="card" onClick={() => navigate("/food-list")}>
            <h3>Food List</h3>
            <p>Browse your food database.</p>
        </div>
    );

    //render user profile card
    const renderUserProfile = (data) => (
        <div className="card" onClick={() => navigate("/user-profile")}>
            <h3>{data.username || "User Profile"}</h3>
            <p>View or update your account information.</p>
        </div>
    );

    return (
        <div>
            <h2>Dashboard</h2>
            <FetchDataFromApi
                endpoint="/api/dashboard/"
                renderData={(data) => (
                    <div className="dashboard-grid">
                        {renderMacros(data)}
                        {renderWeight(data)}
                        {renderFoodList()}
                        {renderUserProfile(data)}
                    </div>
                )}
            />
        </div>
    );
};

export default Dashboard;