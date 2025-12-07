import axios from "axios";

const apiRequest = axios.create({
  baseURL: "http://localhost:5005/",
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
