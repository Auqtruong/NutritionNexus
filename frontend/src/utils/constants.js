//map labels to category names
export const categoryMap = {
    "Food Name": "food_name",
    Calories: "calories",
    Carbohydrates: "carbohydrates",
    Protein: "protein",
    Fat: "fat",
    Date: "date",
};

export const mapCategory = (label) => categoryMap[label] || label;
