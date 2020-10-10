import React, { useState } from "react";
import {
  Card,
  TextField,
  Button,
  Grid,
  Slider,
  Input,
  InputAdornment,
} from "@material-ui/core";
import TradingIcon from "@material-ui/icons/LocalAtm";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import Page from "../components/page/Page";

const Trading = () => {
  const [tradeType, setTradeType] = useState("buy");
  const [purchaseBy, setPurchaseBy] = useState("quantity");
  const [orderType, setOrderType] = useState("market");
  const [sliderValue, setSliderValue] = useState(20);

  const handleInputChange = (event) => {
    setSliderValue(event.target.value === "" ? "" : Number(event.target.value));
  };

  const handleBlur = () => {
    if (sliderValue < 0) {
      setSliderValue(0);
    } else if (sliderValue > 100) {
      setSliderValue(100);
    }
  };

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
            Trade Type:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={tradeType}
              exclusive
              onChange={(_event, newValue) =>
                newValue !== null && setTradeType(newValue)
              }
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
              onChange={(_event, newValue) =>
                newValue !== null && setPurchaseBy(newValue)
              }
            >
              <ToggleButton value="quantity">Quantity</ToggleButton>
              <ToggleButton value="value">Value</ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          <Grid item xs={3}>
            number:
          </Grid>
          <Grid item container direction="row" xs={9}>
            <Grid item xs={7} sm={10}>
              <Slider
                // defaultValue={sliderValue}
                value={sliderValue}
                onChange={(_event, newValue) => setSliderValue(newValue)}
                getAriaValueText={valuetext}
                aria-labelledby="discrete-slider"
                step={1}
                // marks
                valueLabelDisplay="on"
                min={0}
                max={110}
                style={{ marginTop: "20px" }}
              />
            </Grid>
            <Grid item xs={5} sm={2}>
              <Input
                value={sliderValue}
                // margin="dense"
                onChange={handleInputChange}
                onBlur={handleBlur}
                disableUnderline={true}
                startAdornment={
                  <InputAdornment position="start">
                    <TradingIcon />
                  </InputAdornment>
                }
                inputProps={{
                  step: 1,
                  min: 0,
                  max: 100,
                  type: "number",
                }}
              />
            </Grid>
          </Grid>
          <Grid item xs={12}>
            TODO: Portfolio Allocation
          </Grid>
          <Grid item xs={3}>
            Order Type:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={orderType}
              exclusive
              onChange={(_event, newValue) =>
                newValue !== null && setOrderType(newValue)
              }
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
