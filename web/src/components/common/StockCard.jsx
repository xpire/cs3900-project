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
import { useHistory } from "react-router-dom";
// import styled from "styled-components";

import { ColoredText, StandardCard } from "./styled";

const StyledCard = styled(Card)({ margin: "10px" });

const StockCard = ({ symbol, name, category, price, delta, skeleton }) => {
  let history = useHistory();
  return (
    <StyledCard>
      <CardActionArea onClick={() => history.push(`/stock/${symbol}`)}>
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
                <Grid item>
                  <Typography variant="h4">{symbol}</Typography>
                  {name && <Chip size="small" label={name} />}
                  <br />
                  <Chip size="small" label={category} />
                </Grid>
                <Grid item>
                  <ColoredText
                    color={delta > 0 ? "green" : "red"}
                    variant="h3"
                    align="right"
                  >
                    {`${delta > 0 ? "+" : ""}${delta}%`}
                  </ColoredText>
                </Grid>
                <Grid item xs={12}>
                  <ColoredText
                    color={delta > 0 ? "green" : "red"}
                    variant="h4"
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
            <Button
              size="small"
              color="primary"
              onClick={() => {
                console.log("TODO: call api to add to user's watch list");
              }}
            >
              watch
            </Button>
            <Button
              size="small"
              color="primary"
              onClick={() => history.push(`/trading?symbol=${symbol}`)}
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
