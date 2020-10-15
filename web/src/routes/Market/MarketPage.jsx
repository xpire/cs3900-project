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
  const [filteredData, setFilteredData] = useState(stockData);

  const handleChange = (e) => {
    setSearch(e);
  };

  useEffect(() => {
    setFilteredData(
      search !== ""
        ? stockData.filter(({ symbol }) =>
            symbol.toLowerCase().includes(search.toLowerCase())
          )
        : stockData
    );
  }, [search, stockData]);

  useEffect(() => {
    axios
      .get("stocks/symbols")
      .then((response) => {
        const data = response.data;
        setStockData(data);
        setLoadingSymbols(false);
      })
      .catch((err) => {});
  }, []);

  const [latestPrices, setLatestPrices] = useState(0);

  const getRealTimeStockData = () => {
    const symbols = stockData.map(({symbol}) => symbol ).join("&symbols=");
    axios
      .get(`/stocks/stocks?symbols=${symbols}`)
      .then((response) => {
        const data = response.data;
        const data2 = data.map(({curr_close_price}, i) => {
          return {symbol: symbols[i], price:curr_close_price}
        })
        console.log(data2);
        setLatestPrices(data2);
        setLoading(false);
      })
      .catch((err) => console.log(err));
  }

  useEffect(() => {
    console.log('loading symbols? ' + loadingSymbols);
    if (loadingSymbols) {
      return;
    }
      
    getRealTimeStockData();
    const interval = setInterval(getRealTimeStockData, 5000);
    return () => clearInterval(interval);
  }, [stockData, loadingSymbols]);

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
