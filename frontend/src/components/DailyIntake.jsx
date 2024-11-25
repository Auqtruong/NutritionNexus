import React, { useEffect, useState } from "react";
import { fetchWithAuth } from "../utils/auth";

const DailyIntake = () => {
    //track daily intake entries fetched from api
    const [intake, setIntake] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchDailyIntake = async () => {
            try {
                const response = await fetchWithAuth("/api/intake/"); //send GET request to get User's log by using function from auth.js
                if (!response.ok) { //unsuccessful fetch
                    throw new Error("Failed to fetch daily intake data");
                }
                const data = await response.json();
                setIntake(data); //update state with fetched data
            }
            catch (err) {
                setError(err.message); //update state with error message if unsuccessful
            }
        };
        fetchDailyIntake(); //function call
    }, []);

    if (error) {
        return <p>Error: {error}</p>; //return error message if there was any
    }

    return (
        <div>
            <h2>Your Daily Intake</h2>
            {intake.length === 0 ? (<p>No entries found for today.</p>) : (
                <ul>
                    {intake.map((item) => ( //iterate over each item in intake array and create unique key based on id
                        <li key={item.id}>
                            <div> 
                                <h3>{item.food_eaten.name}</h3>
                                <p><strong>Quantity:</strong> {item.food_quantity}g</p>
                                <p><strong>Date:</strong> {item.food_entry_date}</p>
                                <p><strong>Calories:</strong> {item.calories} kcal</p>
                                <p><strong>Carbohydrates:</strong> {item.carbohydrates} g</p>
                                <p><strong>Protein:</strong> {item.protein} g</p>
                                <p><strong>Fat:</strong> {item.fat} g</p>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DailyIntake;