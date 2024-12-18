import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FetchDataFromApi from "./FetchDataFromApi";

const FoodList = ({ searchQuery, sortOptions, filters }) => {
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
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Calories</th>
                            <th>Carbohydrates</th>
                            <th>Protein</th>
                            <th>Fat</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.results.map((food) => (
                            <tr key={food.id} onClick={() => handleFoodClick(food.id)}>
                                <td>{food.name}</td>
                                <td>{food.calories} kcal</td>
                                <td>{food.carbohydrates} g</td>
                                <td>{food.protein} g</td>
                                <td>{food.fat} g</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

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
                queryParams={{
                    search_term: searchQuery || "",
                    sort_category: sortOptions?.category?.toLowerCase() || "name",
                    sort_order: sortOptions?.order?.toLowerCase() || "asc",
                    ...filters,
                }}
                renderData={renderFoodList}
            />
        </div>
    );
};

export default FoodList;