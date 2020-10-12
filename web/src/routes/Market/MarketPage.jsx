import React from "react";
import { Typography, Card, Grid, TextField } from "@material-ui/core";
import { Autocomplete } from "@material-ui/lab";
import matchSorter from "match-sorter";

import Page from "../../components/page/Page";
import StockCard, {
  SkeletonStockCard,
} from "../../components/common/StockCard";

import * as data from "../../utils/stocksList.json"; //TODO: make this an API call

const Market = () => {
  const stockData = data.data.slice(0, 30);
  const filterOptions = (options, { inputValue }) =>
    matchSorter(options, inputValue);
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

            {/* <Typography variant="h2">TODO: [Search bar]</Typography> */}
            {/* </Card> */}
          </Grid>
          <Grid item xs={12}>
            <Typography>
              Your search returned {stockData.length} results.
            </Typography>
          </Grid>
          <Grid item md={4} sm={6} xs={12}>
            <SkeletonStockCard />
          </Grid>
          {stockData.map(({ symbol, type }, index) => {
            return (
              <Grid item md={4} sm={6} xs={12} key={symbol}>
                <StockCard
                  name={symbol}
                  category={type}
                  price="$25,333"
                  delta={index % 2 === 0 ? 25 : -10}
                  key={symbol}
                />
              </Grid>
            );
          })}
        </Grid>
      </div>
    </Page>
  );
};

export default Market;
