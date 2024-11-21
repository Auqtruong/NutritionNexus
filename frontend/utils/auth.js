const API_BASE_URL = "http://127.0.0.1:8000/api/"; //resuable

//login; send user/pass to api/token endpoint, store access and refresh token in local storage
export const login = async (credentials) => {
    const response = await fetch(`${API_BASE_URL}token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(credentials),
    });
    if (response.ok) { //valid response
        const data = await response.json();
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        return data;
    }
    throw new Error("Invalid Credentials")
}

//refreshAccessToken; send refresh token to api/token/refresh endpoint to get new access token
export const refreshAccessToken = async () => {
    
}

//logout; clear from local storage
export const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

//auth check; check if access token exists in local storage
export const isAuthenticated = () => {
    const token = localStorage.getItem("access_token")
    return token ? true : false;
}
