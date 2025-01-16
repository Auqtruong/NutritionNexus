import { useState, useEffect } from "react";
import FetchDataFromApi from "./FetchDataFromApi";

const WeightTracker = ({ sortOptions, filters, onCheckboxChange, onEdit, refreshKey }) => {
    const [currentPage, setCurrentPage] = useState(1); //Track current page; initial page set to 1
    const [dataKey    , setDataKey]     = useState(0); //Track state to force re-render data fetch when refreshKey changes

    useEffect(() => {
        setDataKey((prev) => prev + 1);
    }, [refreshKey]);

    //Render paginated weight log
    const renderWeightLog = (data) => {
        if (!data.results || data.results.length === 0) {
            return <p>No weight entries found.</p>;
        }

        return (
            <div>
                <table className="weight-tracker-table">
                    <thead>
                        <tr>
                            <th>
                                <input
                                    type="checkbox"
                                    onChange={(event) =>
                                        onCheckboxChange(
                                            event.target.checked,
                                            "all",
                                            data.results.map((entry) => entry.id)
                                        )
                                    }
                                />
                            </th>
                            <th>Weight (kg)</th>
                            <th>Date</th>
                            <th>Actions</th> {/* Actions column for Edit button(s) */}
                        </tr>
                    </thead>
                    <tbody>
                        {data.results.map((item) => (
                            <tr key={item.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        onChange={(event) =>
                                            onCheckboxChange(
                                                event.target.checked,
                                                item.id
                                            )
                                        }
                                    />
                                </td>
                                <td>{item.weight}</td>
                                <td>{new Date(item.weight_entry_date).toLocaleDateString()}</td>
                                <td>
                                    <button onClick={() => onEdit(item)}>
                                        Edit
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Pagination controls */}
                <div>
                    <button
                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                        disabled={!data.previous} //Disable if no previous page exists
                    >
                        Previous
                    </button>
                    <button
                        onClick={() => setCurrentPage((prev) => prev + 1)}
                        disabled={!data.next} //Disable if no next page exists
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
                queryParams={{
                    sort_category: sortOptions?.category?.toLowerCase() || "weight_entry_date",
                    sort_order: sortOptions?.order?.toLowerCase() || "desc",
                    ...filters, //pass filters to backend for processing
                }}
                key={dataKey}
                renderData={renderWeightLog}
            />
        </div>
    );
};

export default WeightTracker;