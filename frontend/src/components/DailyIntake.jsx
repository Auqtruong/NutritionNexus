import { useNavigate } from "react-router-dom";
import FetchDataFromApi from "./FetchDataFromApi";

const DailyIntake = ({ searchQuery, sortOptions }) => {
    const navigate = useNavigate();

    const handleFoodClick = (id) => {
        navigate(`/food/${id}`); //Navigate to FoodDetailPage for the food that was clicked
    };

    const renderDailyIntake = (data) => {
        if (data.length === 0) {
            return <p>No entries found for today.</p>;
        }

        return (
            <ul>
                {data.map((item) => ( //iterate over each item in intake array and create unique key based on id
                    <li key={item.id} onClick={() => handleFoodClick(item.food_eaten.id)}>
                        <div>
                            <h3>{item.food_eaten.name}</h3>
                            <p><strong>Quantity:</strong> {item.food_quantity}g</p>
                            <p><strong>Date:</strong> {item.food_entry_date}</p>
                            <p><strong>Calories:</strong> {item.calories} kcal</p>
                            <p><strong>Carbohydrates:</strong> {item.carbohydrates} g</p>
                            <p><strong>Protein:</strong> {item.protein} g</p>
                            <p><strong>Fat:</strong> {item.fat} g</p>
                        </div>
                    </li>
                ))}
            </ul>
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