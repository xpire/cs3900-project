import React, { useState } from "react";
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

// import * as data from "../../utils/stocksList.json"; //TODO: make this an API call
import { useEffect } from "react";

const Market = () => {
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
    fetch("http://127.0.0.1:8000/symbols")
      .then((response) => response.json())
      .then((data) => {
        setStockData(data);
        setLoading(false);
      });
  }, []);

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
              : `Your search returned ${
                  filteredData.length
                } result${filteredData.length !== 1 && "s"}.`}
          </Typography>
        </Grid>
      </Grid>
      <CardGrid data={filteredData} />
    </Page>
  );
};

export default Market;
