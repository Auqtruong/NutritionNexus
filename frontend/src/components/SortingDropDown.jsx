import { useState } from "react";
import PropTypes from "prop-types";

const SortingDropDown = ({ categories, onSortChange }) => {
    const [sortCategory, setSortCategory]   = useState(""); //track category to sort by
    const [sortOrder   , setSortOrder]      = useState(""); //track ordering to sort by

    const orders = ["Ascending", "Descending"];

    //Mapping of user-friendly categories to backend-compatible field names
    const categoryMapping = {
        "Food Name": "name",
        "Calories": "calories",
        "Protein": "protein",
        "Carbohydrates": "carbohydrates",
        "Fat": "fat",

        "Daily Intake Food Name": "food_eaten__name",
        "Daily Intake Food Calories": "food_eaten__calories",
        "Date": "food_entry_date",

        "Weight": "weight",
        "Weight Entry Date": "weight_entry_date",
    };


    const handleSort = () => {
        if (sortCategory && sortOrder) {
            const backendField = categoryMapping[sortCategory];
            if (backendField) {
                onSortChange({ category: backendField, order: sortOrder }); // Pass mapped category and order
            }
        }
    };

    return (
        <div className="sorting-dropdown">
            {/* choose category */}
            <select
                value={sortCategory}
                onChange={(event) => setSortCategory(event.target.value)}
            >
                {/* default option */}
                <option value="">Select Category</option>
                {categories.map((category) => ( //create a category for each option
                    <option key={category} value={category}>
                        {category}
                    </option>
                ))}
            </select>
            {/* choose order */}
            <select
                value={sortOrder}
                onChange={(event) => setSortOrder(event.target.value)}
            >
                {/* default option */}
                <option value="">Select Order</option>
                {orders.map((order) => ( //create a category for each option
                    <option key={order} value={order.toLowerCase()}>
                        {order}
                    </option>
                ))}
            </select>
            {/* disable button if either options are empty */}
            <button onClick={handleSort} disabled={!sortCategory || !sortOrder}>
                Apply
            </button>
        </div>
    );
};

// Prop types validation
SortingDropDown.propTypes = {
    categories: PropTypes.arrayOf(PropTypes.string).isRequired,
    onSortChange: PropTypes.func.isRequired,
};

// Default props (if no categories are provided)
SortingDropDown.defaultProps = {
    categories: [],
    onSortChange: () => {},
};

export default SortingDropDown;