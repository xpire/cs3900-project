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
import Page from "../../components/page/Page";

const Trading = () => {
  const defaultState = {
    tradeType: "buy",
    purchaseBy: "quantity",
    orderType: "market",
    quantity: 20,
  };
  const [state, setState] = useState(defaultState);
  // const set = (stateString) => (value) => setState({ ...state, [stateString]: value})
  const setTradeType = (value) => setState({ ...state, tradeType: value });
  const setPurchaseBy = (value) => setState({ ...state, purchaseBy: value });
  const setOrderType = (value) => setState({ ...state, orderType: value });
  const setQuantity = (value) => setState({ ...state, quantity: value });

  const handleInputChange = (event) => {
    setQuantity(event.target.value === "" ? "" : Number(event.target.value));
  };

  const handleBlur = () => {
    if (state.quantity < 0) {
      setQuantity(0);
    } else if (state.quantity > 100) {
      setQuantity(100);
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
            <TextField variant="outlined" label="Symbol" />
          </Grid>
          <Grid item xs={3}>
            Trade Type:
          </Grid>
          <Grid item xs={9}>
            <ToggleButtonGroup
              value={state.tradeType}
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
              value={state.purchaseBy}
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
                // defaultValue={quantity}
                value={state.quantity}
                onChange={(_event, newValue) => setQuantity(newValue)}
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
                value={state.quantity}
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
              value={state.orderType}
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
              value={`$${123 * state.quantity}`}
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
              <Button onClick={() => setState(defaultState)}>clear</Button>
            </Grid>
            <Grid item>
              <Button onClick={() => {}}>Submit</Button>
            </Grid>
          </Grid>
        </Grid>
      </Card>
    </Page>
  );
};

export default Trading;
