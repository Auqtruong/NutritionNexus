import { useState } from "react";
import UserProfile from "../components/UserProfile";
import UpdateAccountModal from "../components/UpdateAccountModal";
import DeleteAccountModal from "../components/DeleteAccountModal";
import ProfilePictureModal from "../components/ProfilePictureModal";

const UserProfilePage = () => {
    const [isUpdateModalOpen, setIsUpdateModalOpen]                 = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen]                 = useState(false);
    const [isProfilePictureModalOpen, setIsProfilePictureModalOpen] = useState(false);
    const [refreshKey, setRefreshKey]                               = useState(0);

    //Modal handlers
    const handleOpenUpdateModal = () => {
        setIsUpdateModalOpen(true);
    };

    const handleCloseUpdateModal = () => {
        setIsUpdateModalOpen(false);
    };

    const handleOpenDeleteModal = () => {
        setIsDeleteModalOpen(true);
    };

    const handleCloseDeleteModal = () => {
        setIsDeleteModalOpen(false);
    };

    const handleOpenProfilePictureModal = () => {
        setIsProfilePictureModalOpen(true);
    };

    const handleCloseProfilePictureModal = () => {
        setIsProfilePictureModalOpen(false);
    };

    return (
        <div className="user-profile-page">
            <h1>User Profile</h1>

            <UserProfile 
                onEdit={handleOpenUpdateModal} 
                refreshKey={refreshKey} 
            />

            <button className="profile-picture-button" onClick={handleOpenProfilePictureModal}>
                Update Profile Picture
            </button>

            <button className="delete-account-button" onClick={handleOpenDeleteModal}>
                Delete Account
            </button>

            <UpdateAccountModal
                isOpen={isUpdateModalOpen}
                onClose={handleCloseUpdateModal}
                setRefreshKey={setRefreshKey}
            />

            <DeleteAccountModal
                isOpen={isDeleteModalOpen}
                onClose={handleCloseDeleteModal}
            />

            <ProfilePictureModal
                isOpen={isProfilePictureModalOpen}
                onClose={handleCloseProfilePictureModal}
                setRefreshKey={setRefreshKey}
            />
        </div>
    );
};

export default UserProfilePage;
