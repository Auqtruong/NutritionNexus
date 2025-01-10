import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { fetchWithAuth } from "../utils/auth";

const UpdateWeightModal = ({ isOpen = false, onClose = () => {}, weightEntry = null, setRefreshKey }) => {
    const [weight, setWeight] = useState(""); //holds the weight input
    const [date  , setDate]   = useState(""); //holds the optional date input

    //Pre-fill forms with weight and date of selected entry on weightEntry change
    useEffect(() => {
        if (weightEntry) {
            setWeight(weightEntry.weight || "");
            setDate(weightEntry.date || "");
        }
    }, [weightEntry]);

    //Update the selected weight
    const handleUpdateWeight = async () => {
        if (!weight) {
            alert("Weight is required.");
            return;
        }

        try {
            const response = await fetchWithAuth(`/api/weight/update/${weightEntry.id}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    weight: parseFloat(weight),
                    date: date || null,
                }),
            });

            if (response.ok) { //successful weight entry update
                alert("Weight updated successfully.");
                onClose();
                setRefreshKey((prev) => prev + 1); //refresh weight log

            } 
            else {
                const errorData = await response.json();
                alert(errorData.error || "Failed to update weight.");
            }
        } 
        catch (error) {
            console.error("Error updating weight:", error);
            alert("An error occurred while updating the weight.");
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>
                    {/* &times is nicer looking X for close buttons */}
                    &times;
                </button>
                <h2>Update Weight</h2>
                <div className="form-group">
                    {/* Weight input */}
                    <label htmlFor="weight">Weight (lbs):</label>
                    <input
                        type="number"
                        id="weight"
                        placeholder="Enter updated weight in lbs"
                        value={weight}
                        onChange={(event) => setWeight(event.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    {/* Date input */}
                    <label htmlFor="date">Date (optional):</label>
                    <input
                        type="date"
                        id="date"
                        value={date}
                        onChange={(event) => setDate(event.target.value)}
                    />
                </div>
                <div className="modal-actions">
                    <button onClick={handleUpdateWeight}>
                        Update Weight
                    </button>
                    <button onClick={onClose}>
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
};

//Validation
UpdateWeightModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    weightEntry: PropTypes.shape({
        id: PropTypes.number.isRequired,
        weight: PropTypes.number.isRequired,
        date: PropTypes.string,
    }),
    setRefreshKey: PropTypes.func.isRequired, //callback to refresh weight log
};

export default UpdateWeightModal;
