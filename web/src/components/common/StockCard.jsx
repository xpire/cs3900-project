import React from "react";
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
import { useHistory, Link } from "react-router-dom";
// import styled from "styled-components";
import { useSnackbar } from "notistack";

import { ColoredText, StandardCard } from "./styled";
import axios from "../../utils/api";
import useHandleSnack from "../../hooks/useHandleSnack";
import TradingHoursIndicator from "../common/TradingHoursIndicator";

const StyledCard = styled(Card)({ margin: "10px" });

/* Sample Parameters:
<StockCard
  symbol={"ABCDEF"}
  name={"this is a sample"}
  category={"ASX"}
  price={"12345.67"}
  delta={999.99}
  key={"sample"}
  skeleton={false}
/> */

const StockCard = ({
  symbol,
  name,
  category,
  price,
  delta,
  online,
  skeleton,
  watchButton = true,
}) => {
  let history = useHistory();
  const { enqueueSnackbar } = useSnackbar();
  const handleSnack = useHandleSnack();

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
                    >
                      {`${delta > 0 ? "+" : ""}${delta}%`}
                    </ColoredText>
                  </Grid>
                </Grid>
                <Grid item xs={12}>
                  <ColoredText
                    color={delta > 0 ? "green" : "red"}
                    variant="h3"
                    align="right"
                  >
                    {`$${price}`}
                  </ColoredText>
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

export default StockCard;
