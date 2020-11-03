import axios from "axios";
/**
 * A custom axios instance where the baseURL of API endpoint is defined
 */
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/",
  timeout: 10000,
});

export default axiosInstance;
