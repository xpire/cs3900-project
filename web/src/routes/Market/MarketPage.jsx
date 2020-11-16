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
import { useSelector } from "react-redux";

const Market = () => {
  const [search, setSearch] = useState("");
  const { data, is_loading: loading } = useSelector((state) => state.stocks);

  const stockData = loading
    ? [...Array(12)].map((_) => {
        return { skeleton: true };
      })
    : data;

  const handleChange = (e) => {
    setSearch(e);
  };

  const [filteredData, setFilteredData] = useState(stockData);
  useEffect(() => {
    setFilteredData(
      search !== ""
        ? stockData.filter(({ symbol, exchange, name }) =>
            symbol
              .concat(exchange)
              .concat(name)
              .toLowerCase()
              .includes(search.toLowerCase())
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
                  <IconButton onClick={() => handleChange("")}>
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
