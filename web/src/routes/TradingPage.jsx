import React, { useState } from "react";
import {
  Typography,
  Card,
  TextField,
  Button,
  ButtonGroup,
  Grid,
  Slider,
  CardActions,
} from "@material-ui/core";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";
import { CenteredCard } from "../components/common/styled";

const Trading = () => {
  const [tradeType, setTradeType] = useState("buy");
  const [purchaseBy, setPurchaseBy] = useState("quantity");
  const [orderType, setOrderType] = useState("market");
  const [sliderValue, setSliderValue] = useState(20);

  const valuetext = (t) => `t`;
  return (
    <Page>
      <Card style={{ padding: "25px" }}>
        <Grid
          container
          direction="row"
          justify="center"
          alignItems="center"
          spacing={2}
        >
          <Grid item xs={3}>
            Symbol:
          </Grid>
          <Grid item xs={9}>
            <TextField variant="outlined" label="Symbol" />{" "}
          </Grid>
          <Grid item xs={3}>
            Order Type:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={tradeType}
              exclusive
              onChange={(event, newValue) => setTradeType(newValue)}
            >
              <ToggleButton value="buy">Buy</ToggleButton>
              <ToggleButton value="sell">Sell</ToggleButton>
              <ToggleButton value="short" disabled>
                Short
              </ToggleButton>
              <ToggleButton value="cover" disabled>
                Cover
              </ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          <Grid item xs={3}>
            Purchase by:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={purchaseBy}
              exclusive
              onChange={(event, newValue) => setPurchaseBy(newValue)}
            >
              <ToggleButton value="quantity">Quantity</ToggleButton>
              <ToggleButton value="value">Value</ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          <Grid item xs={3}>
            number:
          </Grid>
          <Grid item xs={9}>
            <Slider
              value={sliderValue}
              onChange={(event, newValue) => setSliderValue(newValue)}
              getAriaValueText={valuetext}
              aria-labelledby="discrete-slider"
              valueLabelDisplay="auto"
              step={1}
              // marks
              valueLabelDisplay="on"
              min={0}
              max={110}
              style={{ marginTop: "20px" }}
            />
          </Grid>
          <Grid item xs={12}>
            TODO: Portfolio Allocation
          </Grid>
          <Grid item xs={3}>
            Price:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={orderType}
              exclusive
              onChange={(event, newValue) => setOrderType(newValue)}
            >
              <ToggleButton value="market">Market</ToggleButton>
              <ToggleButton value="limit">Limit</ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          <Grid item xs={3} />
          <Grid item xs={9}>
            <TextField
              label="Price"
              value={`$${123 * sliderValue}`}
              InputProps={{
                readOnly: true,
              }}
              variant="outlined"
            />
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-end"
            alignItems="flex-end"
          >
            <Grid item>
              <Button>clear</Button>
            </Grid>
            <Grid item>
              <Button>Submit</Button>
            </Grid>
          </Grid>
        </Grid>
      </Card>
    </Page>
  );
};

export default Trading;
