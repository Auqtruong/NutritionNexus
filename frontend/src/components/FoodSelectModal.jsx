import { useState, useEffect } from "react";
import { fetchWithAuth } from "../utils/auth";

const FoodSelectModal = ({ onClose }) => {
    const [foodList, setFoodList] = useState([]); //holds list of food items from food list
    const [searchQuery, setSearchQuery] = useState(""); //track search bar value
    const [selectedFoodId, setSelectedFoodId] = useState(null); //track food id of selected food item to add
    const [quantity, setQuantity] = useState(100); //default 100g

    //Fetch food list to display
    useEffect(() => {
        const fetchFoodList = async () => {
            try {
                const response = await fetchWithAuth("/api/foods/");
                if (response.ok) { //Food list successfully fetched
                    const data = await response.json();
                    setFoodList(data.results);
                }
            }
            catch (error) {
                console.error("Failed to fetch food list:", error);
            }
        };
        fetchFoodList();
    }, []);

    //Handle adding food to daily intake
    const handleAddToIntake = async () => {
        if (!selectedFoodId) {
            alert("Please select a food item.");
            return;
        }

        try {
            const response = await fetchWithAuth("/api/intake/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ food_id: selectedFoodId, food_quantity: quantity }), //Default quantity is 100g
            });

            if (response.ok) {//food item successfully added to daily intake
                alert("Food added to daily intake!");
                onClose();
            } 
            else {
                const errorData = await response.json();
                alert(errorData.error || "Failed to add food to daily intake.");
            }
        } 
        catch (error) {
            console.error("Error adding food to daily intake:", error);
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>Select Food</h2>
                <input
                    type="text"
                    placeholder="Search for food..."
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                />
                <ul>
                    {foodList
                        .filter((food) =>
                            food.name.toLowerCase().includes(searchQuery.toLowerCase()) //match food names to query, case-insensitive
                        )
                        .map((food) => ( //create a list of all food items
                            <li
                                key={food.id}
                                onClick={() => setSelectedFoodId(food.id)}
                                style={{
                                    cursor: "pointer",
                                    fontWeight:
                                        selectedFoodId === food.id ? "bold" : "normal",
                                }}
                            >
                                {food.name} (Calories: {food.calories}, Protein: {food.protein}g, Carbs: {food.carbohydrates}g, Fat: {food.fat}g)
                            </li>
                        ))}
                </ul>

                {selectedFoodId && (
                    <div>
                        <label htmlFor="quantity">Quantity (g):</label>
                        <input
                            type="number"
                            id="quantity"
                            min="1"
                            placeholder="Enter quantity (g)"
                            value={quantity}
                            onChange={(event) => setQuantity(event.target.value)}
                        />
                    </div>
                )}

                <button onClick={handleAddToIntake}>Add to Intake</button>
                <button onClick={onClose}>Cancel</button> 
            </div>
        </div>
    );
};

export default FoodSelectModal;
