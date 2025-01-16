import { useState } from "react";
import PropTypes from "prop-types";
import { fetchWithAuth } from "../utils/auth";
import { useNavigate } from "react-router-dom";

const DeleteAccountModal = ({ isOpen = false, onClose = () => {} }) => {
    const [password, setPassword] = useState(""); //track password input
    const [error, setError]       = useState("");
    const navigate                = useNavigate();

    //Handle account deletion
    const handleDeleteAccount = async (event) => {
        event.preventDefault();

        if (!password.trim()) {
            setError("Password cannot be empty.");
            return;
        }

        try {
            const response = await fetchWithAuth("/api/user/delete/", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ password }),
            });

            if (response.ok) { //account successfully deleted
                alert("Account deleted successfully!");
                localStorage.removeItem("token");
                navigate("/register"); //redirect to registration page after account deletion
            }
            else {
                const data = await response.json();
                setError(data.error || "Failed to delete account.");
            }
        }
        catch (error) {
            console.error("Error deleting account: ", error);
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
                    <h2>Confirm Account Deletion</h2>
                    <button className="close-button" onClick={onClose}>
                        &times;
                    </button>
                </div>
                <div className="modal-body">
                    <p>Deleting your account is permanent and cannot be undone.</p>
                    <p>Please enter your password to confirm deletion:</p>
                    <form onSubmit={handleDeleteAccount}>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                        />
                        {error && <p className="error-message">{error}</p>}
                        <div className="modal-actions">
                            <button type="submit" className="delete-button">
                                Delete Account
                            </button>
                            <button
                                type="button" className="cancel-button" onClick={onClose}>
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

//Validation
DeleteAccountModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired
};

export default DeleteAccountModal;
