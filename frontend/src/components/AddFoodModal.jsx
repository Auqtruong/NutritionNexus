import { useState } from "react";
import { fetchWithAuth } from "../utils/auth";

const AddFoodModal = ({ isOpen = false, onClose = () => {}, setRefreshKey }) => {
    const [searchQuery  , setSearchQuery]   = useState(""); //track search bar value
    const [searchResults, setSearchResults] = useState([]); //holds list of food items returned from /api/nutrition
    const [selectedFoods, setSelectedFoods] = useState([]); //track foods user selected to add/save

    //Handle search logic
    const handleSearch = async () => {
        try {
            const response = await fetchWithAuth(`/api/nutrition/?query=${encodeURIComponent(searchQuery)}`);
            if (response.ok) { //successful fetch
                const data = await response.json();
                setSearchResults(data.items || []);
            } 
            else {
                console.error("Error fetching nutrition data:", response.statusText);
            }
        } 
        catch (error) {
            console.error("Error fetching nutrition data:", error);
        }
    };

    //Handle food selection for adding foods
    const toggleFoodSelection = (food) => {
        setSelectedFoods((prev) => {
            const isSelected = prev.includes(food); //check if food is selected or not

            if (isSelected) {
                //remove already selected foods
                return prev.filter((f) => f !== food);
            }
            else {
                //add the food otherwise
                return [...prev, food];
            }
        });
    };

    //send selected foods to backend to be saved
    const saveSelectedFoods = async () => {
        try {
            const response = await fetchWithAuth("/api/foods/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: searchQuery,
                    items: selectedFoods,
                }),
            });

            if (response.ok) { //succesfully added food(s)
                alert("Foods added successfully.");
                onClose();
                setRefreshKey((prev) => prev + 1); //increment refreshKey
            } 
            else {
                console.error("Error saving selected foods:", response.statusText);
            }
        } 
        catch (error) {
            console.error("Error saving selected foods:", error);
        }
    };

    if (!isOpen) {
        return null; //Only render anything if modal is opened
    }

    return (
        <div className="modal">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>
                    {/* &times is nicer looking X for close buttons */}
                    &times;
                </button>
                <h2>Add New Food</h2>
                <input
                    type="text"
                    placeholder="Search for a food (e.g., apple, banana, chicken breast)"
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                />

                <button onClick={handleSearch}>
                    Search
                </button>
                
                {searchResults.length > 0 && (
                    <div>
                        <h3>Results:</h3>
                        <ul>
                            {searchResults.map((item) => ( //create/render a list item for each food item, along with a checkbox for selection
                                <li key={item.name}>
                                    <input
                                        type="checkbox"
                                        checked={selectedFoods.includes(item)}
                                        onChange={() => toggleFoodSelection(item)}
                                    />
                                    {/* show basic name and calorie information about food items */}
                                    {item.name} - {item.calories} calories
                                </li>
                            ))}
                        </ul>
                        <button onClick={saveSelectedFoods}>
                            Add Selected Foods
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

//Validation
AddFoodModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    setRefreshKey: PropTypes.func.isRequired,
};

export default AddFoodModal;
