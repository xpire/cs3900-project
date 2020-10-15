import React from "react";
import { Grid } from "@material-ui/core";

import StockCard from "./StockCard";

const CardGrid = ({ data, prices, gains}) => {
  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      alignItems="flex-start"
      spacing={0}
    >
      {data.map(({ symbol, exchange, skeleton }, index) => {
        return (
          <Grid item md={4} sm={6} xs={12} key={index}>
            <StockCard
              name={symbol}
              category={exchange}
              price={prices[symbol]?.toFixed(2)}
              delta={gains[symbol]?.toFixed(2)}
              key={index}
              skeleton={skeleton}
            />
          </Grid>
        );
      })}
    </Grid>
  );
};

export default CardGrid;
