import { useState } from "react";
import FoodList from "../components/FoodList";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import SearchBar from "../components/SearchBar";

const FoodListPage = () => {
    const [filters, setFilters] = useState({});
    const [sortOptions, setSortOptions] = useState({ category: "name", order: "asc" });
    const [searchQuery, setSearchQuery] = useState(""); //Keep track of search input

    //Filter Schema
    const filterSchema = [
        { key: "food_name",     label: "Food Name",     type: "text"   },
        { key: "calories_min",  label: "Min Calories",  type: "number" },
        { key: "calories_max",  label: "Max Calories",  type: "number" },
        { key: "carbs_min",     label: "Min Carbs",     type: "number" },
        { key: "carbs_max",     label: "Max Carbs",     type: "number" },
        { key: "protein_min",   label: "Min Protein",   type: "number" },
        { key: "protein_max",   label: "Max Protein",   type: "number" },
        { key: "fat_min",       label: "Min Fat",       type: "number" },
        { key: "fat_max",       label: "Max Fat",       type: "number" },
    ];

    //Handle changes to filters
    const handleFiltersChange = (updatedFilters) => {
        setFilters(updatedFilters);
    };

    //Handle changes to sorting options
    const handleSortChange = (newSortOptions) => {
        setSortOptions(newSortOptions);
    };

    //Handle changes to search input
    const handleSearch = (searchTerm) => {
        setSearchQuery(searchTerm); //Update the search query
        setFilters((prevFilters) => ({
            ...prevFilters,
            food_name: searchTerm, 
        }));
    };

    return (
        <div className="food-list-page">
            <h1>Food List</h1>

            {/* Search Bar */}
            <SearchBar onSearch={handleSearch} />

            {/* Filters */}
            <FilterBar filters={filterSchema} onFilterChange={handleFiltersChange} />

            {/* Sorting */}
            <SortingDropDown
                categories={["Food Name", "Calories", "Carbohydrates", "Protein", "Fat"]}
                onSortChange={handleSortChange}
            />

            {/* Food list with pagination */}
            <FoodList
                searchQuery={searchQuery}
                sortOptions={sortOptions}
                filters={filters}
            />
        </div>
    );
};

export default FoodListPage;
