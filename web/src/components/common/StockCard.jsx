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
import { useHistory } from "react-router-dom";
// import styled from "styled-components";

import { ColoredText } from "./styled";

const StyledCard = styled(Card)({});

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
              <Typography variant="h3">{name}</Typography>
              <Chip size="small" label={category} />
            </Grid>
            <Grid item>
              <ColoredText
                color={delta > 0 ? "green" : "red"}
                variant="h2"
                align="right"
              >
                {delta > 0 && "+"}
                {delta}%
              </ColoredText>
            </Grid>
            <Grid item xs={12}>
              <ColoredText
                color={delta > 0 ? "green" : "red"}
                variant="h3"
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
