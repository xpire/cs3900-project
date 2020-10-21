import { useEffect, useState } from "react";
import axios from "../utils/api";

const useRealTimeStockData = (
  path = "stocks/symbols",
  update = [],
  initialData = [...Array(12)].map((_) => {
    return { skeleton: true };
  }),
  modifier = (x) => x
) => {
  const [loadingSymbols, setLoadingSymbols] = useState(true);
  const [loading, setLoading] = useState(true);

  const [symbols, setSymbols] = useState();

  useEffect(() => {
    axios
      .get(path)
      .then((response) => {
        const data = response.data;
        setSymbols(modifier(data));
        setLoadingSymbols(false);
      })
      .catch((err) => {});
  }, update);

  const [stockData, setStockData] = useState(initialData);

  const getRealTimeStockData = () => {
    if (symbols === undefined) {
      return;
    }

    const s = symbols.map(({ symbol }) => symbol).join("&symbols=");
    axios
      .get(`/stocks/stocks?symbols=${s}`)
      .then((response) => {
        const data = response.data;
        setStockData(data);
        setLoading(false);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    getRealTimeStockData();
    const interval = setInterval(getRealTimeStockData, 5000);
    return () => clearInterval(interval);
  }, [symbols, loadingSymbols]);

  return [stockData, loading];
};

export default useRealTimeStockData;
