import { useState } from "react";
import WeightTracker from "../components/WeightTracker";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import AddWeightModal from "../components/AddWeightModal";
import UpdateWeightModal from "../components/UpdateWeightModal";
import { handleDeleteSelected } from "../utils/handleDeleteSelected";

const WeightTrackerPage = () => {
    const [filters              , setFilters]               = useState({});
    const [sortOptions          , setSortOptions]           = useState({ category: "date", order: "desc" });
    const [isAddModalOpen       , setIsAddModalOpen]        = useState(false);
    const [isUpdateModalOpen    , setIsUpdateModalOpen]     = useState(false);
    const [selectedItems        , setSelectedItems]         = useState(new Set()); //tracks weight entries for deletion
    const [selectedItemToUpdate , setSelectedItemToUpdate]  = useState(null); //track weight entry to update
    const [refreshKey           , setRefreshKey]            = useState(0); //state to trigger refresh after update

    //Handle changes to filters and pass query string to backend
    const handleFiltersChange = (queryString) => {
        setFilters(queryString);
    };

    //Handle changes to sorting options
    const handleSortChange = (newSortOptions) => {
        setSortOptions(newSortOptions);
    };

    //Modal handlers
    const handleOpenAddModal = () => {
        setIsAddModalOpen(true);
    };

    const handleCloseAddModal = () => {
        setIsAddModalOpen(false);
    };

    const handleOpenUpdateModal = (item) => {
        setSelectedItemToUpdate(item);
        setIsUpdateModalOpen(true);
    };

    const handleCloseUpdateModal = () => {
        setSelectedItemToUpdate(null);
        setIsUpdateModalOpen(false);
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
            "/api/weight/delete",
            selectedItems,
            setSelectedItems,
            setRefreshKey
        );
    };

    return (
        <div className="weight-tracker-page">
            <h1>Weight Tracker</h1>

            <button onClick={handleOpenAddModal}>
                Add Weight Entry
            </button>

            <button onClick={handleDelete} disabled={selectedItems.size === 0}>
                Delete Selected
            </button>

            {/* Filtering */}
            <FilterBar onSubmit={handleFiltersChange} />

            {/* Sorting */}
            <SortingDropDown
                categories={[
                    "Weight Entry Date",
                    "Weight"
                ]}
                onSortChange={handleSortChange}
            />

            <WeightTracker
                sortOptions={sortOptions}
                filters={filters}
                onCheckboxChange={handleCheckboxChange}
                onEdit={handleOpenUpdateModal}
                refreshKey={refreshKey}
            />

            <AddWeightModal 
                isOpen={isAddModalOpen} 
                onClose={handleCloseAddModal}
                setRefreshKey={setRefreshKey}
            />

            <UpdateWeightModal
                isOpen={isUpdateModalOpen}
                onClose={handleCloseUpdateModal}
                weightEntry={selectedItemToUpdate}
                setRefreshKey={setRefreshKey}
            />
        </div>
    );
};

export default WeightTrackerPage;
