import { useState, useEffect } from "react";
import { fetchWithAuth, logout } from "../utils/auth";

const UserProfile = () => {
    const [userData, setUserData] = useState({ username: "", weight: "" }); //fetched data
    const [isEditing, setIsEditing] = useState(false); //display profile vs. form
    const [formData, setFormData] = useState({ username: "", password: "" }); //keep track of edits
    const [showDelete, setShowDelete] = useState(false);
    const [deletePass, setDeletePass] = useState(""); //track password being entered for account deletion
    const [loading, setLoading] = useState(true);

    //form validation before updating/deleting
    const validateForm = (fields) => {
        for (const field in fields) {
            if (!fields[field].trim()) {
                return `${field} cannot be empty.`;
            }
        }
        return null; //no empty or invalid fields found
    };

    //check for token expiration
    const handleUnauthorized = (response) => {
        if (response.status === 401) {
            alert("Session expired. Please log in again.");
            logout();
            window.location.href = "/login"; //navigate user to login page after token expires
            return true; //response was 401 unauthorized
        }
        return false;
    }

    //handle input data
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    //fetch user profile data
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetchWithAuth("/api/user/profile/");

                if (handleUnauthorized(response)) return;

                if (response.ok) { //data successfully fetched
                    const data = await response.json();
                    setUserData(data); //update user profile with fetched data
                }
            }
            catch (error) {
                console.error("Failed to fetch user data: ", error);
            }
            finally {
                setLoading(false); //stop loading after fetching
            }
        };
        fetchUserData();
    }, []);

    //handles updating user profile data
    const handleUpdate = async (event) => {
        event.preventDefault();
        const error = validateForm({ username: formData.username, password: formData.password });
        if (error) { //invalid/empty data found
            alert(error);
            return;
        }

        try {
            const response = await fetchWithAuth("/api/user/update/", {
                method: "PUT",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (handleUnauthorized(response)) return;

            if (response.ok) {
                setUserData({ ...userData, username: formData.username || userData.username });
                setIsEditing(false);
                alert("Profile updated successfully!");
            }
            else {
                alert("Failed to update profile.");
            }
        }
        catch (error) {
            console.error("Error updating user profile: ", error);
        }
    };

    //handles account deletion
    const handleAccountDeletion = async (event) => {
        event.preventDefault();
        const error = validateForm({ password: deletePass });
        if (error) {
            alert(error);
            return;
        }

        try {
            const response = await fetchWithAuth("/api/user/delete/", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ password: deletePass }),
            });
            if (handleUnauthorized(response)) return;

            if (response.ok) { //account successfully deleted
                alert("Account deleted successfully!");
                localStorage.removeItem("token");
                window.location.href = "/register"; //refresh and navigate user to registration page after their account is deleted
            }
            else {
                const data = await response.json();
                alert(data.error || "Failed to delete account."); //display error if deletion failed
            }
        }
        catch (error) {
            console.error("Error deleting account: ", error);
        }
    };

    if (loading) {
        return <p>Loading...</p>; //display a loading message
    }

    //render
    return (
        <div className="user-profile">
            <div className="profile-picture">
                {/* TO DO */}
            </div>
            {/* Default to showing user info, otherwise show editing forms */}
            <div className="profile-info">
                {!isEditing ? (
                    <>
                        <h2>Username: {userData.username}</h2>
                        <p>Password: ********</p>
                        <p>Last Recorded Weight: {userData.weight || "N/A"}</p>
                        <button onClick={() => setIsEditing(true)}>Edit Profile</button>
                        <button onClick={logout}>Log Out</button>
                        <button onClick={() => setShowDelete(true)}>Delete Account</button>
                    </>
                ) : (
                    <form onSubmit={handleUpdate} className="edit-profile">
                        <label>
                            Username:
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleInputChange}
                                placeholder={userData.username}
                            />
                        </label>
                        <label>
                            Password:
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                placeholder="********"
                            />
                        </label>
                        <button type="submit">Save Changes</button>
                        <button onClick={() => setIsEditing(false)}>Cancel</button>
                    </form>
                )}
                {/* Delete Account Prompt */}
                {showDelete && (
                    <div className="delete-prompt">
                        <p>Enter your password to confirm account deletion:</p>
                        <form onSubmit={handleAccountDeletion}>
                            <input
                                type="password"
                                placeholder="Password"
                                value={deletePass}
                                onChange={(event) => setDeletePass(event.target.value)}
                            />
                            <button type="submit">Delete Account</button>
                            <button onClick={() => setShowDelete(false)}>Cancel</button>
                        </form>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserProfile;