import axios from "axios";
import axiosRetry, {
  isNetworkError,
  isIdempotentRequestError,
} from "axios-retry";

/**
 * A custom axios instance where the baseURL of API endpoint is defined
 */
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/",
  timeout: 10000,
});

axiosRetry(axiosInstance, {
  retries: 3,
  retryCondition: (error) =>
    isNetworkError(error) ||
    isIdempotentRequestError(error) ||
    (error.response.status >= 400 && error.response.status <= 401),
});

export default axiosInstance;
