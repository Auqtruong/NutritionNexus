import { useState } from "react";
import DailyIntake from "../components/DailyIntake";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import SearchBar from "../components/SearchBar";

const DailyIntakePage = () => {
    const [filters, setFilters] = useState({});
    const [sortOptions, setSortOptions] = useState({ category: "date", order: "desc" });
    const [searchQuery, setSearchQuery] = useState(""); //Keep track of search input

    //Filter Schema
    const filterSchema = [
        { key: "food_name",     label: "Food Name",     type: "text", placeholder: "Search foods..." },
        { key: "date_min",      label: "Date From",     type: "date"   },
        { key: "date_max",      label: "Date To",       type: "date"   },
        { key: "calories_min",  label: "Min Calories",  type: "number" },
        { key: "calories_max",  label: "Max Calories",  type: "number" },
    ];

    //Handle changes to filters
    const handleFiltersChange = (updatedFilters) => {
        setFilters(updatedFilters); //Update filter values
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
        <div className="daily-intake-page">
            <h1>Your Daily Intake</h1>

            {/* Search Bar */}
            <SearchBar onSearch={handleSearch} />

            {/* Filters */}
            <FilterBar filters={filterSchema} onFilterChange={handleFiltersChange} />

            {/* Sorting */}
            <SortingDropDown
                categories={["Food Name", "Calories", "Carbohydrates", "Protein", "Fat", "Date"]}
                onSortChange={handleSortChange}
            />

            {/* Daily intake list */}
            <DailyIntake
                searchQuery={searchQuery}
                sortOptions={sortOptions}
                filters={filters}
            />
        </div>
    );
};

export default DailyIntakePage;
