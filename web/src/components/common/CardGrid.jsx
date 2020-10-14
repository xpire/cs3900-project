import React from "react";
import { Grid } from "@material-ui/core";

import StockCard from "./StockCard";

const CardGrid = ({ data }) => {
  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      alignItems="flex-start"
      spacing={0}
    >
      {data.map(({ symbol, type, skeleton }, index) => {
        return (
          <Grid item md={4} sm={6} xs={12} key={index}>
            <StockCard
              name={symbol}
              category={type}
              price="$25,333"
              delta={index % 2 === 0 ? 25 : -10}
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
