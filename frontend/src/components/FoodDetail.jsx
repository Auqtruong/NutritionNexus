import { fetchWithAuth } from "../utils/auth";

const FoodDetail = () => { 
    const [food, setFood]       = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError]     = useState("");
    const { foodId }            = useParams();

    useEffect(() => {
        const fetchFoodDetails = async () => {
            try {
                const response = await fetchWithAuth(`/api/foods/${foodId}/`);
                if (!response.ok) { //unsuccessful fetch
                    throw new Error(`Failed to fetch food details`);
                }
                const data = await response.json();
                setFood(data); //update food details with fetched data
            }
            catch (err) {
                setError(err.message); //update state with error message if unsuccessful
            }
            finally {
                setLoading(false); //data is no longer being loaded regardless of success or failure
            }
        };
        fetchFoodDetails();
    }, [foodId]); //only run on foodId change

    if (loading) return <p>Loading...</p>; //not finished loading/fetching data
    if (error)   return <p>Error: {error}</p>; //display any errors
    if (!food)   return <p>Food details not found.</p>; //no data returned

    return (
        <div className="food-detail">
            <h2>{food.name}</h2>
            <div className="nutrition">
                <p><strong>Calories:</strong> {food.calories} kcal</p>
                <p><strong>Carbohydrates:</strong> {food.carbohydrates} g</p>
                <p><strong>Protein:</strong> {food.protein} g</p>
                <p><strong>Fat:</strong> {food.fat} g</p>
            </div>
        </div>
    );
};

export default FoodDetail;