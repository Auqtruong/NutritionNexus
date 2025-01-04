import { useState } from "react";
import PropTypes from "prop-types";

const SortingDropDown = ({ categories, onSortChange }) => {
    const [sortCategory, setSortCategory] = useState(""); //track category to sort by
    const [sortOrder, setSortOrder] = useState(""); //track ordering to sort by

    const orders = ["Ascending", "Descending"];

    const handleSort = () => {
        if (sortCategory && sortOrder) {
            onSortChange({ category: sortCategory, order: sortOrder }); //pass chosen sorting options back to main function
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
    categories: [
        "name",                   //Food name
        "calories",               //Food calories
        "protein",                //Food protein
        "carbohydrates",          //Food carbohydrates
        "fat",                    //Food fat
        "food_eaten__name",       //Daily intake food name
        "food_eaten__calories",   //Daily intake food calories
        "food_entry_date",        //Daily intake entry date
        "weight",                 //Weight tracker weight
        "weight_entry_date",      //Weight tracker entry date
    ],
    onSortChange: () => {},
};

export default SortingDropDown;