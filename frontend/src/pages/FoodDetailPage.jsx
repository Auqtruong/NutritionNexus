import { useParams } from "react-router-dom";
import FoodDetail from "../components/FoodDetail";

const FoodDetailPage = () => {
    const { foodId } = useParams(); //get food id from URL params

    return (
        <div className="food-detail-page">
            <h1>Food Details</h1>
            <FoodDetail 
                foodId={foodId} 
            />
        </div>
    );
};

export default FoodDetailPage;
