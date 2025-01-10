export const handleDeleteSelected = async (endpoint, selectedItems, setSelectedItems, setRefreshKey = null) => {
    if (selectedItems.size === 0) {
        alert("No items selected for deletion.");
        return;
    }

    const confirmed = window.confirm(
        "Are you sure you want to delete the selected items?"
    );

    if (!confirmed) {
        return;
    }

    try {
        // endpoint varies with page
        const response = await fetchWithAuth(endpoint, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ids: Array.from(selectedItems) }),
        });

        if (response.ok) { //successfully delete food(s)/entries
            alert("Selected items deleted successfully.");
            setSelectedItems(new Set());

            if (setRefreshKey) {
                setRefreshKey((prev) => prev + 1); //increment refreshKey
            }
        } 
        else {
            console.error("Failed to delete items:", response.statusText);
        }
    } 
    catch (error) {
        console.error("Error deleting items:", error);
    }
};
