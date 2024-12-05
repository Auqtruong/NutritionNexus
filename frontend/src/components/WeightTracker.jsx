import { useState } from "react";
import FetchDataFromApi from "./FetchDataFromApi";

const WeightTracker = () => {
    //Track current page; initial page set to 1
    const [currentPage, setCurrentPage] = useState(1);

    //Render weight log entries
    const renderWeightLog = (data) => {
        if (data.results.length === 0) {
            return <p>No weight entries found.</p>;
        }

        return (
            <div>
                <ul>
                    {data.results.map((entry) => (
                        <li key={entry.id}>
                            <div>
                                <p><strong>Date:</strong> {entry.weight_entry_date}</p>
                                <p><strong>Weight:</strong> {entry.weight} kg</p>
                            </div>
                        </li>
                    ))}
                </ul>
                {/* Pagination controls */}
                <div>
                    <button
                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                        disabled={!data.previous} // Disable if no previous page exists
                    >
                        Previous
                    </button>
                    <button
                        onClick={() => setCurrentPage((prev) => prev + 1)}
                        disabled={!data.next} // Disable if no next page exists
                    >
                        Next
                    </button>
                </div>
            </div>
        );
    };

    return (
        <div>
            <h2>Weight Tracker</h2>
            {/* Fetch and render weight tracker data */}
            <FetchDataFromApi
                endpoint="/api/weight/"
                page={currentPage}
                renderData={renderWeightLog}
            />
        </div>
    );
};

export default WeightTracker;