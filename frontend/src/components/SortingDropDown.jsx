import { useState } from "react";
import { mapCategory } from "../utils/constants";
import PropTypes from "prop-types";

const SortingDropDown = ({ categories, onSortChange }) => {
    const [sortCategory, setSortCategory] = useState(""); //track category to sort by
    const [sortOrder, setSortOrder] = useState(""); //track ordering to sort by

    const orders = ["Ascending", "Descending"];

    const handleSort = () => {
        if (sortCategory && sortOrder) {
            const apiCategory = mapCategory[sortCategory];
            onSortChange({ category: apiCategory, order: sortOrder }); //pass chosen sorting options back to main function
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

//validate prop types
SortingDropDown.propTypes = {
    categories: PropTypes.arrayOf(PropTypes.string), 
    onSortChange: PropTypes.func,
};

//default values if props are not explicitly passed to component
SortingDropDown.defaultProps = {
    categories: ["Food Name", "Calories", "Carbohydrates", "Protein", "Fat", "Date"],
    onSortChange: () => {},
};

export default SortingDropDown;