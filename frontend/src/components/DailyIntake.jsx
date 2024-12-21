import { useNavigate } from "react-router-dom";
import FetchDataFromApi from "./FetchDataFromApi";

const DailyIntake = ({ searchQuery, sortOptions }) => {
    const navigate = useNavigate();

    const handleFoodClick = (id) => {
        navigate(`/food/${id}`); //Navigate to FoodDetailPage for the food that was clicked
    };

    const renderDailyIntake = (data) => {
        if (!data || data.length === 0) {
            return <p>No entries found for today.</p>;
        }

        return (
            <table className="daily-intake-table">
                <thead>
                    <tr>
                        <th>Food Name</th>
                        <th>Quantity (g)</th>
                        <th>Date</th>
                        <th>Calories (kcal)</th>
                        <th>Carbohydrates (g)</th>
                        <th>Protein (g)</th>
                        <th>Fat (g)</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => ( //iterate over every entry and create a row
                        <tr
                            key={item.id}
                            onClick={() => handleFoodClick(item.food_eaten.id)}
                            style={{ cursor: "pointer" }}
                        >
                            <td>{item.food_eaten.name}</td>
                            <td>{item.food_quantity}</td>
                            <td>{new Date(item.food_entry_date).toLocaleDateString()}</td>
                            <td>{item.calories}</td>
                            <td>{item.carbohydrates}</td>
                            <td>{item.protein}</td>
                            <td>{item.fat}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div>
            {/* Fetch and render daily intake data */}
            <FetchDataFromApi
                endpoint="/api/intake/"
                queryParams={{
                    search_term: searchQuery || "",
                    sort_category: sortOptions?.category?.toLowerCase() || "date",
                    sort_order: sortOptions?.order?.toLowerCase() || "desc",
                    ...filters,
                }}
                renderData={renderDailyIntake}
            />
        </div>
    );
};

export default DailyIntake;