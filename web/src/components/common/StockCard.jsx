import React, { useEffect, useState, useRef } from "react";
import PropTypes from "prop-types";
import {
  Card,
  CardActionArea,
  CardActions,
  Button,
  CardContent,
  Typography,
  Chip,
  Grid,
  styled,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { Link } from "react-router-dom";
// import styled from "styled-components";

import ColoredText, { useColoredText } from "../common/ColoredText";
import useHandleSnack from "../../hooks/useHandleSnack";
import TradingHoursIndicator from "../common/TradingHoursIndicator";

const StyledCard = styled(Card)({ margin: "10px" });

/**
 * A StockCard component to be used in CardGrid.
 */
const StockCard = ({
  symbol,
  name,
  category,
  price,
  delta,
  online,
  skeleton,
  watchButton,
}) => {
  const handleSnack = useHandleSnack();
  const [deltaColor] = useColoredText(price);
  // const myDelta = useDelta(price);
  // const [deltaColor, setDeltaColor] = useState(0);

  // const fadeInAndOut = (flag) => {
  //   setDeltaColor(flag);
  //   setTimeout(() => setDeltaColor(0), 1000);
  // };

  // useEffect(() => {
  //   console.log("delta effect");
  //   if (myDelta && myDelta.prev && myDelta.prev !== "NaN") {
  //     const prev = parseFloat(myDelta.prev.replace(/[%$]*/g, ""));
  //     const curr = parseFloat(myDelta.curr.replace(/[%$]*/g, ""));
  //     console.log({ prev, curr });
  //     if (prev < curr) {
  //       console.log("highlight Green");
  //       fadeInAndOut(1);
  //     } else {
  //       console.log("highlight Red");
  //       fadeInAndOut(-1);
  //     }
  //   }
  // }, [delta]);

  return (
    <StyledCard>
      <CardActionArea component={Link} to={`/stock/${symbol}`}>
        <CardContent>
          <Grid
            container
            direction="row"
            justify="space-between"
            alignItems="flex-start"
          >
            {skeleton ? (
              <Grid item xs={12}>
                <Skeleton variant="rect" width="100%" height={108} />
              </Grid>
            ) : (
              <>
                <Grid item xs={12} spacing={1} container>
                  <Grid item>{name && <Chip size="small" label={name} />}</Grid>
                  <Grid item>
                    <Chip size="small" label={category} />
                  </Grid>
                  <Grid item>
                    <TradingHoursIndicator online={online} />
                  </Grid>
                </Grid>
                <Grid container alignItems="flex-end" justify="space-between">
                  <Grid item>
                    <Typography variant="h4">{symbol}</Typography>
                  </Grid>
                  <Grid item>
                    <ColoredText
                      color={delta > 0 ? "green" : "red"}
                      variant="h4"
                      align="right"
                      delta={deltaColor}
                    >
                      {`${delta > 0 ? "+" : ""}${delta}%`}
                    </ColoredText>
                  </Grid>
                </Grid>
                <Grid item xs={12} container direction="row-reverse">
                  <Grid item>
                    <ColoredText
                      color={delta > 0 ? "green" : "red"}
                      variant="h3"
                      align="right"
                      delta={deltaColor}
                    >
                      {`$${price}`}
                    </ColoredText>
                  </Grid>
                </Grid>
              </>
            )}
          </Grid>
        </CardContent>
      </CardActionArea>
      <CardActions>
        {skeleton ? (
          <Skeleton variant="rect" height={30} width="100%" />
        ) : (
          <>
            {watchButton && (
              <Button
                size="small"
                color="primary"
                onClick={() =>
                  handleSnack(`/watchlist?symbol=${symbol}`, "post")
                }
              >
                watch
              </Button>
            )}
            <Button
              size="small"
              color="primary"
              to={`/trade?symbol=${symbol}`}
              component={Link}
            >
              trade
            </Button>
          </>
        )}
      </CardActions>
    </StyledCard>
  );
};

StockCard.propTypes = {
  /** The Stock's symbol code (e.g. "ABCDEF") */
  symbol: PropTypes.string,
  /** The Stock's name (e.g. "Apple Industry") */
  name: PropTypes.string,
  /** The Stock's Stock Exchange Acronym (e.g. "ASX") */
  category: PropTypes.string,
  /** The Stock's current closing price (e.g. "12345.67") */
  price: PropTypes.string,
  /** The Stock's current daily change percentage (e.g. 999.99) */
  delta: PropTypes.string,
  /** Whether the Stock's Stock Market is open for trading */
  online: PropTypes.bool,
  /** Whether this card should display the Skeleton component to signify loading */
  skeleton: PropTypes.bool,
  /** Whether to show the watch button */
  watchButton: PropTypes.bool,
};

StockCard.defaultProps = {
  watchButton: true,
};

export default StockCard;
