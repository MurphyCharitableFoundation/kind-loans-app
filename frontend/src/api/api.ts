import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: { "Content-Type": "application/json" },
});

export const fetchData = async (endpoint: string) => {
    const response = await apiClient.get(endpoint);
    return response.data;
};
