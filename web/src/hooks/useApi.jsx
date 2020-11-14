import { useState, useEffect } from "react";
import axios from "../utils/api";

/**
 * A React Hook to simplify state and lifecycle management of an API call
 * @param {string} url endpoint where data is served
 * @param {array} update array of dependencies which will reload API
 * @param {array} initial array of initial datapoints
 * @param {func} modifier modifier function applied to data before it is set by useState
 */
const useApi = (url, update = [], initial = [], modifier = (e) => e) => {
  const [data, setData] = useState(initial);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const getData = () => {
    setLoading(true);
    axios
      .get(url)
      .then((response) => {
        setData(modifier(response.data));
        setLoading(false);
      })
      .catch((err) => setError(true));
  };
  useEffect(getData, update);

  return [data, loading, error, getData];
};

export default useApi;
