import React from "react";
import { Grid } from "@material-ui/core";

import StockCard from "./StockCard";
import { format } from "../../utils/formatter";

const CardGrid = ({ data }) => {
  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      alignItems="flex-start"
      spacing={0}
    >
      {data.map(
        (
          {
            symbol,
            name,
            exchange,
            curr_day_close,
            prev_day_close,
            skeleton,
            is_trading,
          },
          index
        ) => {
          let delta = null;
          // TODO maybe it's undefined
          if (curr_day_close !== undefined && prev_day_close !== undefined) {
            delta = (100 * (curr_day_close - prev_day_close)) / prev_day_close;
          }
          return (
            <Grid item md={4} sm={6} xs={12} key={index}>
              <StockCard
                symbol={symbol}
                name={name}
                category={exchange}
                price={format(curr_day_close)} //{curr_day_close?.toFixed(2)}
                delta={format(delta)} //{delta?.toFixed(2)}
                key={index}
                online={is_trading}
                skeleton={skeleton}
              />
            </Grid>
          );
        }
      )}
    </Grid>
  );
};

export default CardGrid;
