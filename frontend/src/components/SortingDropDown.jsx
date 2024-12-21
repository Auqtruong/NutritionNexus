import { useState } from "react";
import { categoryMap } from "../utils/categoryMap";

const SortingDropDown = ({ categories, onSortChange }) => {
    const [sortCategory, setSortCategory] = useState(""); //track category to sort by
    const [sortOrder, setSortOrder] = useState(""); //track ordering to sort by

    const orders = ["Ascending", "Descending"];

    const handleSort = () => {
        if (sortCategory && sortOrder) {
            const apiCategory = categoryMap[sortCategory];
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
                    <option key={category} value={category.toLowerCase()}>
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

export default SortingDropDown;