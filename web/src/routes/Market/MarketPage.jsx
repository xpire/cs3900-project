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
import useRealTimeStockData from "../../hooks/useRealTimeStockData";


const CheckWatchlist = async () => {
  return await axios
    .get("/watchlist")
    .then(response => response.data)
}

const Market = () => {
  const [search, setSearch] = useState("");
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, loading] = useRealTimeStockData();

  const handleChange = (e) => {
    setSearch(e);
  };

  useEffect(() => {
    CheckWatchlist().then(data => {
      setWatchlist(data.map(item => item.symbol))
    })
  }, [])
  
  const clickedWatchlist = () => {
    CheckWatchlist().then(data => {
      setWatchlist(data.map(item => item.symbol))
    })
  }


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
            aria-label="search"
          />
        </Grid>
        <Grid item xs={12}>
          <Typography>
            {loading
              ? `Loading...`
              : `Your search returned ${filteredData.length} result${filteredData.length !== 1 ? "s" : ""
              }.`}
          </Typography>
        </Grid>
      </Grid>
      <CardGrid data={filteredData} renderWatchlist={true} watchlist={[watchlist, clickedWatchlist]} />
    </Page>
  );
};

export default Market;
