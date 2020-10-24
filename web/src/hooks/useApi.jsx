import { useState, useEffect } from "react";
import axios from "../utils/api";

const useApi = (url, update = []) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  useEffect(() => {
    axios
      .get(url)
      .then((response) => {
        setData(response.data);
        setLoading(true);
      })
      .catch((err) => setError(true));
  }, update);

  return [data, loading, error];
};

export default useApi;
