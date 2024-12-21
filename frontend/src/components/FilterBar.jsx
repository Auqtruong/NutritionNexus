import { useState } from "react";
import { categoryMap } from "../utils/categoryMap";

//utility component for generic/dynamic filtering across different pages with different categories
const FilterBar = ({ filters, onFilterChange }) => {
    const [filterValues, setFilterValues] = useState(() =>
        filters.reduce((aggregator, filter) => {
            aggregator[filter.key] = ""; //initialize all filters with empty values
            return aggregator;
        }, {})
    );

    const handleInputChange = (label, value) => {
        const key = categoryMap[label] || label; //use original key if no mapping exists
        const updatedFilters = { ...filterValues, [key]: value }; //only update changed filters
        setFilterValues(updatedFilters); //update filter state with incoming values
        onFilterChange(updatedFilters); 
    };

    return (
        <div className="filter-bar">
            {filters.map((filter) => ( //loop through filter array and create input fields for each
                <label key={filter.key}>
                    {filter.label}
                    <input
                        type={filter.type}
                        value={filterValues[filter.key]}
                        onChange={(event) => handleInputChange(filter.label, event.target.value)}
                        placeholder={filter.placeholder || ""}
                    />
                </label>
            ))}
        </div>
    );
};

export default FilterBar;