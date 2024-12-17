import FetchDataFromApi from "./FetchDataFromApi";

const Dashboard = () => {
    //render user's daily macros data
    const renderMacros = (data) => {
        return (
            <div>
                <h3>Today's Macros</h3>
                <p>Calories: {data.total_cals} kcal</p>
                <p>Carbohydrates: {data.total_carbs} g</p>
                <p>Protein: {data.total_protein} g</p>
                <p>Fats: {data.total_fat} g</p>
            </div>
        );
    };

    //render user's most recent weight data
    const renderWeight = (data) => {
        return (
            <div>
                <h3>Last Recorded Weight</h3>
                <p>
                    {/* Use most recent recorded weight and entry date since user might not always update daily weight value */}
                    Last Recorded Weight: {data.last_rec_weight !== null ? `${data.last_rec_weight} kg` : "No data available"}
                </p>
                <p>
                    Date: {data.last_weight_date !== null ? data.last_weight_date : "No data available"}
                </p>
            </div>
        );
    };

    return (
        <div>
            <h2>Dashboard</h2>
            {/* Fetch and render user's total daily macros and last weight data */}
            <FetchDataFromApi
                endpoint="/api/dashboard/"
                renderData={(data) => (
                    <div>
                        {renderMacros(data)}
                        {renderWeight(data)}
                    </div>
                )}
            />
        </div>
    );
};

export default Dashboard;