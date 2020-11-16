import React from "react";
import PropTypes from "prop-types";
import { Grid } from "@material-ui/core";

import StockCard from "./StockCard";
import { format } from "../../utils/formatter";

const CardGrid = ({ data, watchButton }) => {
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
            <Grid item lg={4} md={6} sm={6} xs={12} key={index}>
              <StockCard
                symbol={symbol}
                name={name}
                category={exchange}
                price={format(curr_day_close)}
                delta={format(delta)}
                key={symbol}
                online={is_trading}
                skeleton={skeleton}
                watchButton={watchButton}
              />
            </Grid>
          );
        }
      )}
    </Grid>
  );
};

CardGrid.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      /** The Stock's symbol code (e.g. "ABCDEF") */
      symbol: PropTypes.string,
      /** The Stock's name (e.g. "Apple Industry") */
      name: PropTypes.string,
      /** The Stock's Stock Exchange Acronym (e.g. "ASX") */
      exchange: PropTypes.string,
      /** The Stock's current closing price. (equivalent to current trading price) */
      curr_close_price: PropTypes.float,
      /** The Stock's previous closing price (equivalent to yesterday's closing trading price) */
      prev_close_price: PropTypes.float,
      /** Whether this card should display the Skeleton component to signify loading */
      skeleton: PropTypes.bool,
      /** Whether the Stock's Stock Market is open for trading */
      is_trading: PropTypes.bool,
    })
  ),
};

export default CardGrid;
