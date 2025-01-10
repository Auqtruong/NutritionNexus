import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import FetchDataFromApi from "./FetchDataFromApi";

const FoodList = ({ sortOptions, filters, onCheckboxChange, refreshKey }) => {
    const [currentPage, setCurrentPage] = useState(1); //Track current page; initial page set to 1
    const navigate = useNavigate();
    const [dataKey    , setDataKey]     = useState(0); //Track state to force re-render data fetch when refreshKey changes

    useEffect(() => {
        setDataKey((prev) => prev + 1);
    }, [refreshKey]);

    const handleFoodClick = (id) => {
        navigate(`/food/${id}`); //Navigate to FoodDetailPage for the food that was clicked
    };

    //Render paginated list of foods
    const renderFoodList = (data) => {
        if (!data.results || data.results.length === 0) {
            return <p>No food items found.</p>;
        }

        return (
            <div>
                <table className="food-list-table">
                    <thead>
                        <tr>
                            <th>
                                <input
                                    type="checkbox"
                                    onChange={(event) =>
                                        onCheckboxChange(
                                            event.target.checked,
                                            "all",
                                            data.results.map((food) => food.id)
                                        )
                                    }
                                />
                            </th>
                            <th>Name</th>
                            <th>Calories</th>
                            <th>Carbohydrates</th>
                            <th>Protein</th>
                            <th>Fat</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.results.map((food) => (
                            <tr key={food.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        onChange={(event) =>
                                            onCheckboxChange(
                                                event.target.checked,
                                                food.id
                                            )
                                        }
                                    />
                                </td>
                                {/* navigate to FoodDetailpage for food item on click */}
                                <td onClick={() => handleFoodClick(food.id)}>
                                    {food.name}
                                </td>
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
                        disabled={!data.previous} //Disable if no previous page exists
                    >
                        Previous
                    </button>
                    <button
                        onClick={() => setCurrentPage((prev) => prev + 1)}
                        disabled={!data.next} //Disable if no next page exists
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
                    sort_category: sortOptions?.category?.toLowerCase() || "name",
                    sort_order: sortOptions?.order?.toLowerCase() || "asc",
                    ...filters, //pass filters to backend for processing
                }}
                key={dataKey}
                renderData={renderFoodList}
            />
        </div>
    );
};

export default FoodList;