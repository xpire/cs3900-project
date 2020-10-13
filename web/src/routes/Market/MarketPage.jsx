import React, { useState, useEffect } from "react";
import { Typography, Grid, TextField } from "@material-ui/core";
import { Autocomplete } from "@material-ui/lab";
import matchSorter from "match-sorter";

import Page from "../../components/page/Page";
import CardGrid from "../../components/common/CardGrid";

import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

const Market = () => {
  const [loading, setLoading] = useState(true);
  const [visibleData, setVisibleData] = useState([
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
  const stockData = data.data; //.slice(0, 30);
  const filterOptions = (options, { inputValue }) =>
    matchSorter(options, inputValue);
  useEffect(() => {
    setTimeout(() => {
      setVisibleData(stockData);
      setLoading(false);
    }, 1500);
  }, []);
  return (
    <Page>
      <div style={{ padding: "12px" }}>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
          spacing={2}
        >
          <Grid item xs={12}>
            {/* <Card> */}
            <Autocomplete
              filterOptions={filterOptions}
              options={stockData}
              getOptionLabel={(option) => option.symbol}
              style={{ width: 300 }}
              fullWidth
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Combo box"
                  variant="outlined"
                  fullWidth
                />
              )}
            />

            <Typography variant="h2">TODO: [Search bar]</Typography>
            {/* </Card> */}
          </Grid>
          <Grid item xs={12}>
            <Typography>
              {loading
                ? `Loading...`
                : `Your search returned ${visibleData.length} results.`}
            </Typography>
          </Grid>
        </Grid>
        <CardGrid data={visibleData} />
      </div>
    </Page>
  );
};

export default Market;
