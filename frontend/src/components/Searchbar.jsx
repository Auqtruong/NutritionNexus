import { useState } from "react";

const SearchBar = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState(""); //keep track of what is being searched

    const handleSearch = (event) => {
        event.preventDefault(); //prevent page refresh
        onSearch(searchTerm);
    };

    return (
        <form onSubmit={handleSearch} className="search-bar">
            <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)} 
            />
            <button type="submit">Search</button>
        </form>
    );
};

export default SearchBar;