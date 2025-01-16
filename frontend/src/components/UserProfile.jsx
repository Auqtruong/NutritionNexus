import { useState, useEffect } from "react";
import FetchDataFromApi from "./FetchDataFromApi";

const UserProfile = ({ onEdit, refreshKey }) => {
    const [dataKey, setDataKey] = useState(0);

    useEffect(() => {
        setDataKey((prev) => prev + 1);
    }, [refreshKey]);

    //Render user profile
    const renderUserInfo = (data) => {
        if (!data) {
            return <p>Error: Unable to load user data. Please try again later.</p>;
        }

        return (
            <div className="user-profile">
                <div className="profile-picture">
                    <img
                        src={data.profile_picture || "/profile_pictures/default.png"}
                        alt="Profile"
                        className="profile-img"
                    />
                </div>
                {/* Keep password omitted */}
                <div className="profile-info">
                    <h2>Username: {data.username}</h2>
                    <p>Password: ********</p>
                    <p>Last Recorded Weight: {data.last_rec_weight ? `${data.last_rec_weight} lbs` : "N/A"}</p>
                    <button className="edit-button" onClick={onEdit}>
                        {/* Edit icon/button */}
                        <i className="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        );
    };

    return (
        <div>
            <h2>User Profile</h2>
            <FetchDataFromApi
                endpoint="/api/user/profile/"
                key={dataKey}
                renderData={renderUserInfo}
            />
        </div>
    );
};

export default UserProfile;
