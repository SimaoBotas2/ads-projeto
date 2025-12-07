import axios from "axios";

const getApiUrl = () => {
  return window.APP_CONFIG?.API_URL || "http://localhost:5005";
};

const apiRequest = axios.create({
  baseURL: getApiUrl(),
  withCredentials: true,
});

apiRequest.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");

      window.location.href = "/auth";
    }

    return Promise.reject(error);
  }
);

export default apiRequest;
