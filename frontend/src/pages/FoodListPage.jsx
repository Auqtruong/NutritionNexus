import { useState } from "react";
import FoodList from "../components/FoodList";
import FilterBar from "../components/FilterBar";
import SortingDropDown from "../components/SortingDropDown";
import SearchBar from "../components/SearchBar";
import AddFoodModal from "../components/AddFoodModal";
import { fetchWithAuth } from "../utils/auth";

const FoodListPage = () => {
    const [filters, setFilters] = useState({});
    const [sortOptions, setSortOptions] = useState({ category: "name", order: "asc" });
    const [searchQuery, setSearchQuery] = useState(""); //Keep track of search input
    const [isModalOpen, setIsModalOpen] = useState(false); //Keep track of modal visiblity
    const [foodList, setFoodList] = useState([]); //Keep track of foods

    //Filter Schema
    const filterSchema = [
        { key: "food_name", label: "Food Name", type: "text" },
        { key: "calories_min", label: "Min Calories", type: "number" },
        { key: "calories_max", label: "Max Calories", type: "number" },
        { key: "carbs_min", label: "Min Carbs", type: "number" },
        { key: "carbs_max", label: "Max Carbs", type: "number" },
        { key: "protein_min", label: "Min Protein", type: "number" },
        { key: "protein_max", label: "Max Protein", type: "number" },
        { key: "fat_min", label: "Min Fat", type: "number" },
        { key: "fat_max", label: "Max Fat", type: "number" },
    ];

    useEffect(() => {
        const fetchFoodList = async () => {
            try {
                const response = await fetchWithAuth("/api/foods/");
                if (response.ok) { //food list successfully fetched
                    const data = await response.json();
                    setFoodList(data.foods || []);
                }
                else {
                    console.error("Error fetching food list:", response.statusText);
                }
            }
            catch (error) {
                console.error("Error fetching food list:", error)
            }
        };
        fetchFoodList();
    }, []);

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

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    //Handle new foods being selected/added
    const handleFoodsAdded = (newFoods) => {
        setFoodList((prevList) => [...prevList, ...newFoods]);
    };

    return (
        <div className="food-list-page">
            <h1>Food List</h1>

            <button onClick={handleOpenModal}>Add Food</button>

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
                foodList={foodList}
                searchQuery={searchQuery}
                sortOptions={sortOptions}
                filters={filters}
            />
            <AddFoodModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onFoodsAdded={handleFoodsAdded}
            />
        </div>
    );
};

export default FoodListPage;
