import { fetchWithAuth } from "../utils/auth";
import { useState, useEffect } from "react";

const FoodDetail = ({ foodId }) => { 
    const [food   , setFood]    = useState(null);
    const [loading, setLoading] = useState(true);
    const [error  , setError]   = useState("");

    useEffect(() => {
        const fetchFoodDetails = async () => {
            try {
                const response = await fetchWithAuth(`/api/foods/${foodId}/`);
                if (!response.ok) { //unsuccessful fetch
                    throw new Error(`Failed to fetch food details`);
                }
                const data = await response.json();
                setFood(data); //update food details with fetched data
            }
            catch (error) {
                setError(error.message); //update state with error message if unsuccessful
            }
            finally {
                setLoading(false); //data is no longer being loaded regardless of success or failure
            }
        };
        fetchFoodDetails();
    }, [foodId]); //only run on foodId change

    if (loading) return <p>Loading...</p>; //not finished loading/fetching data
    if (error)   return <p>Error: {error}</p>; //display any errors
    if (!food)   return <p>Food details not found.</p>; //no data returned

    return (
        <div className="food-detail">
            <h2 className="food-name">{food.name}</h2>
            <div className="nutrition-label">
                <div className="nutrition-section">
                    <p><strong>Calories:</strong> {food.calories} kcal</p>
                    <p><strong>Carbohydrates:</strong> {food.carbohydrates} g</p>
                    <p><strong>Protein:</strong> {food.protein} g</p>
                    <p><strong>Fat:</strong> {food.fat} g</p>
                    <p><strong>Saturated Fat:</strong> {food.fat_saturated} g</p>
                </div>
                <div className="nutrition-section">
                    <p><strong>Sodium:</strong> {food.sodium} mg</p>
                    <p><strong>Potassium:</strong> {food.potassium} mg</p>
                    <p><strong>Cholesterol:</strong> {food.cholesterol} mg</p>
                    <p><strong>Fiber:</strong> {food.fiber} g</p>
                    <p><strong>Sugar:</strong> {food.sugar} g</p>
                </div>
            </div>
        </div>
    );
};

export default FoodDetail;