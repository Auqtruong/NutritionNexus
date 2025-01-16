import { useState } from "react";
import PropTypes from "prop-types";
import { fetchWithAuth } from "../utils/auth";

const AddWeightModal = ({ isOpen = false, onClose = () => {}, setRefreshKey }) => {
    const [weight, setWeight] = useState(""); //holds the weight input
    const [date  , setDate]   = useState(""); //holds the optional date input

    //Handle form submission to add weight
    const handleAddWeight = async () => {
        if (!weight) {
            alert("Weight is required.");
            return;
        }

        try {
            const response = await fetchWithAuth("/api/weight/record/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    weight: parseFloat(weight),
                    date: date || null, // Send null if date is not provided
                }),
            });

            if (response.ok) { //successfully added weight entry
                alert("Weight recorded successfully.");
                onClose();
                setRefreshKey((prev) => prev + 1); //increment refreshKey
            } 
            else {
                const errorData = await response.json();
                alert(errorData.error || "Failed to record weight.");
            }
        } 
        catch (error) {
            console.error("Error recording weight:", error);
            alert("An error occurred while recording the weight.");
        }
    };

    if (!isOpen) {
        return null; //Only render anything if modal is opened
    }

    return (
        <div className="modal">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>
                    {/* &times is nicer looking X for close buttons */}
                    &times;
                </button>
                <h2>Record Weight</h2>
                <div className="form-group">
                    {/* Weight input */}
                    <label htmlFor="weight">Weight (lbs):</label>
                    <input
                        type="number"
                        id="weight"
                        placeholder="Enter your weight in lbs"
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
                    <button onClick={handleAddWeight}>
                        Add Weight
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
AddWeightModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    setRefreshKey: PropTypes.func.isRequired,
};

export default AddWeightModal;
