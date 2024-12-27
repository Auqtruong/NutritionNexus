const API_BASE_URL = "http://127.0.0.1:8000/api/"; //resuable

//login; send user/pass to api/token endpoint, store access and refresh token in local storage
export const login = async (credentials) => {
    const response = await fetch(`${API_BASE_URL}token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
    });
    if (response.ok) { //valid response
        const data = await response.json();
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        return data;
    }
    throw new Error("Invalid Credentials")
};

//refreshAccessToken; send refresh token to api/token/refresh endpoint to get new access token
export const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
        throw new Error("No refresh token available");
    }
    const response = await fetch(`${API_BASE_URL}token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
    });
    if (response.ok) { //valid response
        const data = await response.json();
        localStorage.setItem("access_token", data.access);
        return data.access;
    }
};

//logout; clear from local storage
export const logout = async () => {
    try {
        const refresh_token = localStorage.getItem("refresh_token");
        if (refresh_token) {
            const response = await fetch("/api/logout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ refresh: refresh_token }),
            });

            if (!response.ok) {
                console.error("Failed to logout on the server:", response.status, response.statusText);
            }
        }
    } catch (error) {
        console.error("Error during logout:", error);
    } finally {
        //clear local storage tokens regardless of API success
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
    }
};

//auth check; check if access token exists in local storage
export const isAuthenticated = () => {
    const token = localStorage.getItem("access_token")
    return token ? true : false;
};

//fetchWithAuth; make authenticated fetch request
export const fetchWithAuth = async (url, options = {}) => {
    let accessToken = localStorage.getItem("access_token");
    const defaultHeaders = {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json"
    };

    try {
        //try to make request with current access token
        const response = await fetch(`${API_BASE_URL}${url}`, {
            ...options,
            headers: { ...defaultHeaders, ...options.headers },
        });

        //on failure, try to refresh token and retry request
        if (response.status === 401) { //unauthorized
            accessToken = await refreshAccessToken();
            const retryResponse = await fetch(`${API_BASE_URL}${url}`, {
                ...options,
                headers: {
                    ...defaultHeaders,
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            return retryResponse; //return retried response with refreshed token
        }
        return response; //return original attempt if initially successful
    }

    catch (error) {
        throw new Error("Failed to make authenticated request")
    }
};