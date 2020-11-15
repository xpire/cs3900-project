import { useEffect, useState } from "react";
import axios from "../utils/api";

const useRealTimeStockData = (
  path = "/stocks",
  update = [],
  initialData = [...Array(12)].map((_) => {
    return { skeleton: true };
  }),
  modifier = (x) => x
) => {
  const [loadingSymbols, setLoadingSymbols] = useState(true);
  const [loading, setLoading] = useState(true);

  const [symbols, setSymbols] = useState();

  const updateSymbols = () =>
    axios
      .get(path)
      .then((response) => {
        const data = response.data;
        setSymbols(modifier(data));
        setLoadingSymbols(false);
      })
      .catch((err) => {});

  useEffect(() => {
    updateSymbols();
  }, update);

  const [stockData, setStockData] = useState(initialData);

  const getRealTimeStockData = () => {
    if (symbols === undefined) {
      return;
    }

    const s = symbols.map(({ symbol }) => symbol).join("&symbols=");
    if (symbols.length > 0) {
      axios
        .get(`/stocks/real_time?symbols=${s}`)
        .then((response) => {
          const data = response.data;
          setStockData(data);
          setLoading(false);
        })
        .catch((err) => console.log(err));
    } else {
      // fix error when attempting to GET `/stocks/real_time?symbolss=`
      setStockData([]);
      setLoading(false);
    }
  };

  useEffect(() => {
    getRealTimeStockData();
    const interval = setInterval(getRealTimeStockData, 5000);
    return () => clearInterval(interval);
  }, [symbols, loadingSymbols]);

  return [stockData, loading, updateSymbols];
};

export default useRealTimeStockData;
