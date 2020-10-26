import { useState, useEffect } from "react";
import axios from "../utils/api";

const useApi = (url, update = [], initial = [], modifier = (e) => e) => {
  const [data, setData] = useState(initial);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  useEffect(() => {
    setLoading(true);
    axios
      .get(url)
      .then((response) => {
        setData(modifier(response.data));
        setLoading(false);
      })
      .catch((err) => setError(true));
  }, update);

  return [data, loading, error];
};

export default useApi;
