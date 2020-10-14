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

const StockCard = ({ name, category, price, delta, skeleton }) => {
  let history = useHistory();
  return (
    <StyledCard>
      <CardActionArea onClick={() => history.push(`/stock/${name}`)}>
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
                  <Typography variant="h4">{name}</Typography>
                  <Chip size="small" label={category} />
                </Grid>
                <Grid item>
                  <ColoredText
                    color={delta > 0 ? "green" : "red"}
                    variant="h3"
                    align="right"
                  >
                    {delta > 0 && "+"}
                    {delta}%
                  </ColoredText>
                </Grid>
                <Grid item xs={12}>
                  <ColoredText
                    color={delta > 0 ? "green" : "red"}
                    variant="h4"
                    align="right"
                  >
                    {price}
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
            <Button size="small" color="primary">
              watch
            </Button>
            <Button size="small" color="primary">
              trade
            </Button>
          </>
        )}
      </CardActions>
    </StyledCard>
  );
};

export default StockCard;
