import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/",
  timeout: 5000,
  // headers: {'X-Custom-Header': 'foobar'}
});

export default axiosInstance;
