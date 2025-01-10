import { useState } from "react";
import DailyIntake from "../components/DailyIntake";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import FoodSelectModal from "../components/FoodSelectModal";
import { handleDeleteSelected } from "../utils/handleDeleteSelected";

const DailyIntakePage = () => {
    const [filters      , setFilters]       = useState({});
    const [sortOptions  , setSortOptions]   = useState({ category: "date", order: "desc" });
    const [isModalOpen  , setIsModalOpen]   = useState(false); //Keep track of modal visibility
    const [selectedItems, setSelectedItems] = useState(new Set()); //track selected entries for deletion
    const [refreshKey   , setRefreshKey]    = useState(0); //state to trigger refresh after update


    //Handle changes to filters and pass query string to backend
    const handleFiltersChange = (queryString) => {
        setFilters(queryString);
    };

    //Handle changes to sorting options
    const handleSortChange = (newSortOptions) => {
        setSortOptions(newSortOptions);
    };

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleCheckboxChange = (isChecked, idOrAll, ids = []) => {
        setSelectedItems((prev) => {
            const updatedSet = new Set(prev);
            if (idOrAll === "all") {
                ids.forEach((id) => {
                    if (isChecked) {
						updatedSet.add(id);
					}
                    else {
						updatedSet.delete(id);
					}
                });
            } 
			else {
                if (isChecked) {
					updatedSet.add(idOrAll);
				}
                else {
					updatedSet.delete(idOrAll);
				}
            }
            return updatedSet;
        });
    };

    //Handle deletes
    const handleDelete = () => {
        handleDeleteSelected(
            "/api/intake/delete",
            selectedItems,
            setSelectedItems,
            setRefreshKey
        );
    };

    return (
        <div className="daily-intake-page">
            <h1>Your Daily Intake</h1>
			
			<button onClick={handleOpenModal}>
                Add Food
            </button>

            {/* Only allow delete button if there are Daily Intake entries */}
            <button onClick={handleDelete} disabled={selectedItems.size === 0}>
                Delete Selected
            </button>

            {/* Filtering */}
            <FilterBar onSubmit={handleFiltersChange} />
			
			{/* Sorting */}
            <SortingDropDown
                categories={[
                    "Daily Intake Food Name",
                    "Daily Intake Food Calories",
                    "Carbohydrates",
                    "Protein",
                    "Fat",
                    "Date"
                ]}
                onSortChange={handleSortChange}
            />

            <DailyIntake
                sortOptions={sortOptions}
                filters={filters}
                onCheckboxChange={handleCheckboxChange}
                refreshKey={refreshKey}
            />

            <FoodSelectModal
				isOpen={isModalOpen}
				onClose={handleCloseModal}
                setRefreshKey={setRefreshKey}
			/>
        </div>
    );
};

export default DailyIntakePage;
