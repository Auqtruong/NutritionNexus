import { useState } from "react";
import PropTypes from "prop-types";

//utility component for generic/dynamic filtering across different pages with different categories
const FilterBar = ({ onSubmit }) => {
    const [input, setInput] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        if (onSubmit) {
            onSubmit(input.trim());
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
        >
            <input
                type="text"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Filter entries (e.g name:chicken, calories>100)"
            />
            <button type="submit">
                Apply
            </button>
        </form>
    );
};

//validate prop types
FilterBar.propTypes = {
    onSubmit: PropTypes.func.isRequired
};

export default FilterBar;