import { useState } from "react";
import PropTypes from "prop-types";
import { fetchWithAuth } from "../utils/auth";

const ProfilePictureModal = ({ isOpen = false, onClose = () => {}, setRefreshKey }) => {
    const [file, setFile]       = useState(null);
    const [error, setError]     = useState("");
    const [success, setSuccess] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError("");
        setSuccess("");
    };

    const handleUpload = async (event) => {
        event.preventDefault();

        if (!file) {
            setError("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("profile_picture", file);

        try {
            const response = await fetchWithAuth("/api/user/upload-profile-picture/", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setSuccess("Profile picture uploaded successfully!");
                setFile(null);
                setRefreshKey((prev) => prev + 1); //increment refreshKey
            }
            else {
                const data = await response.json();
                setError(data.error || "Failed to upload profile picture.");
            }
        }
        catch (error) {
            console.error("Error uploading profile picture:", error);
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
                    <h2>Upload Profile Picture</h2>
                    <button className="close-button" onClick={onClose}>
                        &times;
                    </button>
                </div>
                <div className="modal-body">
                    <form onSubmit={handleUpload}>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                        />
                        {error && <p className="error-message">{error}</p>}
                        {success && <p className="success-message">{success}</p>}
                        <div className="modal-actions">
                            <button type="submit" className="upload-button">
                                Upload
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

//Validation
ProfilePictureModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    setRefreshKey: PropTypes.func.isRequired,
};

export default ProfilePictureModal;
