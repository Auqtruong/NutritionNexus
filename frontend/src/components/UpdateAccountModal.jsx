import { useState } from "react";
import PropTypes from "prop-types";
import { fetchWithAuth } from "../utils/auth";

const UpdateAccountModal = ({ isOpen = false, onClose = () => {}, setRefreshKey }) => {
    const [username, setUsername] = useState(""); //track updated username
    const [password, setPassword] = useState(""); //track updated password
    const [error, setError] 	  = useState("");
    const [success, setSuccess]   = useState("");

    const handleUpdateAccount = async (event) => {
        event.preventDefault();

		//Empty fields check
        if (!username.trim() && !password.trim()) {
            setError("Please provide a new username or password.");
            return;
        }

        const updateData = {}; //Hold data that will be updated
		
		
        if (username.trim()) {
			updateData.username = username.trim();
		}
        if (password.trim()) {
			updateData.password = password.trim();
		}

        try {
            const response = await fetchWithAuth("/api/user/update/", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updateData),
            });

            if (response.ok) { //account successfully updated
                setSuccess("Account updated successfully!");
                setUsername("");
                setPassword("");
                setError("");
                onClose();
                setRefreshKey((prev) => prev + 1);
            } 
			else {
                const data = await response.json();
                setError(data.error || "Failed to update account.");
            }
        } 
		catch (err) {
            console.error("Error updating account:", err);
            setError("An error occurred. Please try again later.");
        }
    };

    if (!isOpen) {
        return null; //Only render modal when it's open
    }

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h2>Update Account</h2>
                    <button className="close-button" onClick={onClose}>
                        &times;
                    </button>
                </div>
                <div className="modal-body">
                    <form onSubmit={handleUpdateAccount}>
                        <div>
                            <label htmlFor="username">New Username</label>
                            <input
                                type="text"
                                id="username"
                                placeholder="Enter new username"
                                value={username}
                                onChange={(event) => setUsername(event.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="password">New Password</label>
                            <input
                                type="password"
                                id="password"
                                placeholder="Enter new password"
                                value={password}
                                onChange={(event) => setPassword(event.target.value)}
                            />
                        </div>
                        {error && <p className="error-message">{error}</p>}
                        {success && <p className="success-message">{success}</p>}
                        <div className="modal-actions">
                            <button type="submit" className="update-button">
                                Update Account
                            </button>
                            <button type="button" className="cancel-button" onClick={onClose}>
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

//Valiation
UpdateAccountModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    setRefreshKey: PropTypes.func.isRequired,
};

export default UpdateAccountModal;
