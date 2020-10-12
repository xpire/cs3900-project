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

import { ColoredText } from "./styled";

const StyledCard = styled(Card)({});

export const SkeletonStockCard = () => {
  return (
    <StyledCard>
      <CardActionArea>
        <CardContent>
          <Grid
            container
            direction="row"
            justify="space-between"
            alignItems="flex-start"
          >
            <Grid item>
              <Skeleton variant="text" width={105} height={42} />
              <Skeleton variant="text" width={105} height={24} />
            </Grid>
            <Grid item>
              <Skeleton variant="text" width={116} height={56} />
              <Skeleton variant="text" />
            </Grid>
            <Grid item xs={12}>
              <Skeleton variant="text" height={42} />
            </Grid>
          </Grid>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Skeleton variant="text" height={24} width="100%" />
      </CardActions>
    </StyledCard>
  );
};

const StockCard = ({ name, category, price, delta }) => {
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
          </Grid>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          watch
        </Button>
        <Button size="small" color="primary">
          trade
        </Button>
      </CardActions>
    </StyledCard>
  );
};

export default StockCard;
