import { Link, useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

const Navbar = ({ userData }) => {
    const navigate  = useNavigate();
    const [dropdownOpen, setDropdownOpen] = useState(false); //toggle dropdown

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    }

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <nav className="navbar">
            {/* Navbar main links */}
            <div className="navbar-links">
                <Link to="/dashboard"       className="navbar-item">Dashboard</Link>
                <Link to="/food-list"       className="navbar-item">Food List</Link>
                <Link to="/daily-intake"    className="navbar-item">Daily Intake</Link>
                <Link to="/weight-tracker"  className="navbar-item">Weight Tracker</Link>
            </div>

            {/* Dropdown */}
            <div className="navbar-profile">
                <div className="profile-dropdown" onClick={toggleDropdown}>
                    <img
                        src={userData.profile_picture || "/profile_pictures/default.png"}
                        alt="Profile"
                        className="profile-icon"
                    />
                    <div className="dropdown-menu">
                        <Link to="/user-profile" className="dropdown-item">View Profile</Link>
                        <button className="dropdown-item" onClick={handleLogout}>Logout</button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
