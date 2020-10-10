import React from "react";
import { Typography, Card, Grid } from "@material-ui/core";

import Page from "../components/page/Page";
import StockCard from "../components/common/StockCard";

import * as data from "../utils/stocksList.json"; //TODO: make this an API call

const Market = () => {
  const stockData = data.data.slice(0, 30);
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
            <Card>
              <Typography variant="h2">TODO: [Search bar]</Typography>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Typography>
              Your search returned {stockData.length} results.
            </Typography>
          </Grid>
          {stockData.map(({ symbol, type }, index) => {
            return (
              <Grid item md={4} sm={6} xs={12}>
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
