import { useState } from "react";
import FoodList from "../components/FoodList";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import AddFoodModal from "../components/AddFoodModal";
import { handleDeleteSelected } from "../utils/handleDeleteSelected";

const FoodListPage = () => {
    const [filters      , setFilters]       = useState({});
    const [sortOptions  , setSortOptions]   = useState({ category: "name", order: "asc" });
    const [isModalOpen  , setIsModalOpen]   = useState(false); //Keep track of modal visiblity
    const [selectedItems, setSelectedItems] = useState(new Set()); //track selected items for deletion
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
                    if (isChecked){
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
            "/api/foods/delete/",
            selectedItems,
            setSelectedItems,
            setRefreshKey
        );
    };

    return (
        <div className="food-list-page">
            <h1>Food List</h1>

            <button onClick={handleOpenModal}>
                Add Food
            </button>

            {/* Only allow delete button if there are food items */}
            <button onClick={handleDelete} disabled={selectedItems.size === 0}>
                Delete Selected
            </button>

            {/* Filtering */}
            <FilterBar onSubmit={handleFiltersChange} />

            {/* Sorting */}
            <SortingDropDown
                categories={[
                    "Food Name", 
                    "Calories", 
                    "Carbohydrates", 
                    "Protein", 
                    "Fat"
                ]}
                onSortChange={handleSortChange}
            />

            {/* Food list with pagination */}
            <FoodList
                sortOptions={sortOptions}
                filters={filters}
                onCheckboxChange={handleCheckboxChange}
                refreshKey={refreshKey}
            />

            <AddFoodModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                setRefreshKey={setRefreshKey}
            />
        </div>
    );
};

export default FoodListPage;
