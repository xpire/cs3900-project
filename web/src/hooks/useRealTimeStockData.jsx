import { useEffect, useState } from "react";
import axios from "../utils/api";

const useRealTimeStockData = (path = "stocks/symbols") => {
  const [loadingSymbols, setLoadingSymbols] = useState(true);
  const [loading, setLoading] = useState(true);

  const [symbols, setSymbols] = useState();

  useEffect(() => {
    axios
      .get(path)
      .then((response) => {
        const data = response.data;
        setSymbols(data);
        setLoadingSymbols(false);
      })
      .catch((err) => {});
  }, []);

  const [stockData, setStockData] = useState([
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
    { skeleton: true },
  ]);

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
