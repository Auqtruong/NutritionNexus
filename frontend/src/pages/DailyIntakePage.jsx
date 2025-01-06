import { useState } from "react";
import DailyIntake from "../components/DailyIntake";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import FoodSelectModal from "../components/FoodSelectModal";
import { fetchWithAuth } from "../utils/auth";

const DailyIntakePage = () => {
    const [filters, setFilters]             = useState({});
    const [sortOptions, setSortOptions]     = useState({ category: "date", order: "desc" });
    const [isModalOpen, setIsModalOpen]     = useState(false); //Keep track of modal visibility
    const [selectedItems, setSelectedItems] = useState(new Set()); //track selected items for checkbox

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

    const handleDeleteSelected = async () => {
        if (selectedItems.size === 0) {
            alert("No entries selected for deletion.");
            return;
        }

        const confirmed = window.confirm(
			"Are you sure you want to delete the selected entries?"
		);
		
        if (!confirmed) {
			return;
		}

        try {
            const response = await fetchWithAuth("/api/intake/delete/", {
                method: "POST",
                headers: { 
					"Content-Type": "application/json" 
				},
                body: JSON.stringify({ ids: Array.from(selectedItems) }),
            });

            if (response.ok) {
                alert("Selected entries deleted successfully.");
                setSelectedItems(new Set());
            } 
			else {
                console.error("Failed to delete entries:", response.statusText);
            }
        } 
		catch (error) {
            console.error("Error deleting entries:", error);
        }
    };

    return (
        <div className="daily-intake-page">
            <h1>Your Daily Intake</h1>
			
			<button onClick={handleOpenModal}>
                Add Food
            </button>

            {/* Only allow delete button if there are Daily Intake entries */}
            <button onClick={handleDeleteSelected} disabled={selectedItems.size === 0}>
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
            />

            <FoodSelectModal
				isOpen={isModalOpen}
				onClose={handleCloseModal}
			/>
        </div>
    );
};

export default DailyIntakePage;
