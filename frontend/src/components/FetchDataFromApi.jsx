import { useState, useEffect } from "react";
import { fetchWithAuth } from "../utils/auth";

const FetchDataFromApi = ({ endpoint, queryParams = {}, page = 1, key, renderData }) => {
    //track data fetched from api
    const [data   , setData]    = useState(null);
    //track whether data is being loaded or not
    const [loading, setLoading] = useState(true);
    const [error  , setError]   = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                //Optional filter parameters and pagination if applicable
                const pagination = page ? { page } : {};
                const params = new URLSearchParams({ ...queryParams, ...pagination }).toString();
                const completeUrl = `${endpoint}?${params}`;

                const response = await fetchWithAuth(completeUrl);
                if (!response.ok) { //unsuccessful fetch
                    throw new Error(`Failed to fetch data from ${completeUrl}`);
                }
                const result = await response.json();
                setData(result); //update state with fetched data
            }
            catch (error) {
                setError(error.message); //update state with error message if unsuccessful
            }
            finally {
                setLoading(false); //data is no longer being loaded regardless of success or failure
            }
        };
        fetchData(); //function call
    }, [endpoint, queryParams, page]); //only run on endpoint, filter, or page change

    if (loading) return <p>Loading...</p>; //not finished loading/fetching data
    if (error)   return <p>Error: {error}</p>; //display any errors
    if (!data)   return <p>No Data Found.</p>; //no data returned

    return <div>{renderData(data)}</div>;
};

export default FetchDataFromApi;