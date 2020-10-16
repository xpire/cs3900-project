import React, { useState, useEffect } from "react";
import {
  Typography,
  Grid,
  Input,
  IconButton,
  InputAdornment,
} from "@material-ui/core";
import ClearIcon from "@material-ui/icons/Clear";

import Page from "../../components/page/Page";
import CardGrid from "../../components/common/CardGrid";
import axios from "../../utils/api";
// import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

const Market = () => {
  const [loadingSymbols, setLoadingSymbols] = useState(true);
  const [loading, setLoading] = useState(true);

  // const stockData = data.data; //.slice(0, 30);
  const [search, setSearch] = useState("");
  const [symbols, setSymbols] = useState();

  useEffect(() => {
    axios
      .get("stocks/symbols")
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
        // const prices = {};
        // const gains = {};

        // data.forEach(({curr_close_price, prev_close_price}, i) => {
        //   prices[symbols[i]] = curr_close_price;
        //   gains[symbols[i]] = 100 * (curr_close_price - prev_close_price) / prev_close_price;
        // })

        // setLatestPrices(prices);
        // setDayGains(gains);
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

  const handleChange = (e) => {
    setSearch(e);
  };

  const [filteredData, setFilteredData] = useState(stockData);
  useEffect(() => {
    setFilteredData(
      search !== ""
        ? stockData.filter(({ symbol }) =>
            symbol.toLowerCase().includes(search.toLowerCase())
          )
        : stockData
    );
  }, [search, stockData]);

  return (
    <Page>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item xs={12}>
          <Input
            fullWidth
            onChange={(e) => handleChange(e.target.value)}
            value={search}
            placeholder="Search"
            endAdornment={
              <InputAdornment position="end">
                {search !== "" && (
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => handleChange("")}
                  >
                    <ClearIcon />
                  </IconButton>
                )}
              </InputAdornment>
            }
            inputProps={{ style: { fontSize: 40 } }}
          />
        </Grid>
        <Grid item xs={12}>
          <Typography>
            {loading
              ? `Loading...`
              : `Your search returned ${filteredData.length} result${
                  filteredData.length !== 1 ? "s" : ""
                }.`}
          </Typography>
        </Grid>
      </Grid>
      <CardGrid data={filteredData} />
    </Page>
  );
};

export default Market;
