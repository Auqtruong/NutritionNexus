import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FetchDataFromApi from "./FetchDataFromApi";

const FoodList = () => {
    //Track current page; initial page set to 1
    const [currentPage, setCurrentPage] = useState(1);
    const navigate = useNavigate();

    const handleFoodClick = (id) => {
        navigate(`/food/${id}`); //Navigate to FoodDetailPage for the food that was clicked
    };

    //Render paginated list of foods
    const renderFoodList = (data) => {
        if (data.results.length === 0) {
            return <p>No food items found.</p>;
        }

        return (
            <div>
                <ul>
                    {data.results.map((food) => ( //Iterate over each item and create unique key based on food id
                        <li key={food.id} onClick={() => handleFoodClick(food.id)}>
                            <div>
                                <h3>{food.name}</h3>
                                <p><strong>Calories:</strong> {food.calories} kcal</p>
                                <p><strong>Carbohydrates:</strong> {food.carbohydrates} g</p>
                                <p><strong>Protein:</strong> {food.protein} g</p>
                                <p><strong>Fat:</strong> {food.fat} g</p>
                            </div>
                        </li>
                    ))}
                </ul>
                {/* Pagination controls */}
                <div>
                    <button
                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                        disabled={!data.previous} // Disable if no previous page exists
                    >
                        Previous
                    </button>
                    <button
                        onClick={() => setCurrentPage((prev) => prev + 1)}
                        disabled={!data.next} // Disable if no next page exists
                    >
                        Next
                    </button>
                </div>
            </div>
        );
    };

    return (
        <div>
            <h2>Food List</h2>
            {/* Fetch and render paginated food data */}
            <FetchDataFromApi
                endpoint="/api/foods/"
                page={currentPage}
                renderData={renderFoodList}
            />
        </div>
    );
};

export default FoodList;