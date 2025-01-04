import { useState } from "react";
import DailyIntake from "../components/DailyIntake";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import FoodSelectModal from "../components/FoodSelectModal";

const DailyIntakePage = () => {
    const [filters, setFilters]         = useState({});
    const [sortOptions, setSortOptions] = useState({ category: "date", order: "desc" });
    const [searchQuery, setSearchQuery] = useState(""); //Keep track of search input
    const [isModalOpen, setIsModalOpen] = useState(false); //Keep track of modal visibility

    const handleOpenModal  = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

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

            {/* Filters */}
            <FilterBar filters={filterSchema} onFilterChange={handleFiltersChange} />

            {/* Sorting */}
            <SortingDropDown
                categories={["Food Name", "Calories", "Carbohydrates", "Protein", "Fat", "Date"]}
                onSortChange={handleSortChange}
            />
            {/* Add Entry */}
            <button onClick={handleOpenModal}>
                + Add Entry
            </button>

            {/* Daily intake list */}
            <DailyIntake
                searchQuery={searchQuery}
                sortOptions={sortOptions}
                filters={filters}
            />

            {/* Food Select Modal */}
            {isModalOpen && <FoodSelecctModal onClose={handleCloseModal} />}
        </div>
    );
};

export default DailyIntakePage;
