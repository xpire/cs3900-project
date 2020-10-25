import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Grid,
  Slider,
  Input,
  InputAdornment,
  LinearProgress,
  CardActions,
  CardContent,
  Typography,
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
} from "@material-ui/core";
import QuantityIcon from "@material-ui/icons/LocalAtm";
import ValueIcon from "@material-ui/icons/MonetizationOn";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import { useLocation, useHistory } from "react-router-dom";
import { useSnackbar } from "notistack";
import { useDebounce } from "react-use";
// import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
// import DateFnsUtils from "@date-io/date-fns";

import Page from "../../components/page/Page";
import axios from "../../utils/api";
import useApi from "../../hooks/useApi";
import AutoCompleteTextField from "../../components/common/AutoCompleteTextField";
import { format } from "../../utils/formatter";
import { StandardCard } from "../../components/common/styled";

const Trading = () => {
  const search = useLocation().search;
  let history = useHistory();
  const [submitLoading, setSubmitLoading] = useState(false);

  // State accessible to users
  const defaultState = {
    symbol: new URLSearchParams(search).get("symbol"),
    tradeType: "buy",
    purchaseBy: "quantity",
    orderType: "market",
    quantity: 20,
    // date: new Date(),
  };

  const [state, setState] = useState(defaultState);
  const setSymbol = (value) => {
    setState({ ...state, symbol: value });
    history.push(`?symbol=${value}`);
    console.log({ state });
  };
  const setTradeType = (value) => setState({ ...state, tradeType: value });
  const setPurchaseBy = (value) => setState({ ...state, purchaseBy: value });
  const setQuantity = (value) => setState({ ...state, quantity: value });
  const setOrderType = (value) => setState({ ...state, orderType: value });

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

  // API calls
  const [locked, lockedLoading] = useApi(`/user`); // check if functionality is locked
  const [portfolioData, portfolioLoading] = useApi(`/portfolio`); // check owned stock for sell and cover
  const [portfolioStats, portfolioStatsLoading] = useApi(`/portfolio/stats`); // check overall stats
  const [rawCommission, rawCommissionLoading] = useApi(
    `/stocks/stocks?symbols=${state.symbol}`,
    [
      //check current close price for stock
      state.symbol,
    ],
    0.005,
    (data) => data[0].commission
  );
  const [closePrice, closePriceLoading] = useApi(
    `/stocks/stocks?symbols=${state.symbol}`,
    [
      //check current close price for stock
      state.symbol,
    ],
    100,
    (data) => data[0].curr_close_price
  );

  // state inaccessible to user
  const [maxValue, setMaxValue] = useState(100);
  const [portfolioAllocation, setPortfolioAllocation] = useState(50);
  const [commission, setCommission] = useState(1.005);
  const [price, setPrice] = useState(1000);
  const [finalQuantity, setFinalQuantity] = useState(20);
  const [previousBalance, setPreviousBalance] = useState(100);

  const loading =
    lockedLoading ||
    portfolioLoading ||
    portfolioStatsLoading ||
    rawCommissionLoading ||
    closePriceLoading;

  // update state for user input
  useEffect(() => {
    if (!loading) {
      setCommission(
        state.tradeType === "buy" || state.tradeType === "short"
          ? 1 + rawCommission // buy  and short
          : 1 - rawCommission // sell and cover
      );
      switch (state.tradeType) {
        case "buy":
          setMaxValue(
            Math.floor(
              state.purchaseBy === "quantity"
                ? portfolioStats.balance / closePrice
                : portfolioStats.balance
            )
          );
          break;
        case "sell":
          const longData = portfolioData.long.find(
            ({ symbol }) => symbol === state.symbol
          );
          longData?.owned &&
            setMaxValue(
              state.purchaseBy === "quantity"
                ? longData.owned
                : longData.owned * closePrice
            );
          break;
        case "short":
          setMaxValue(
            Math.floor(
              state.purchase === "quantity"
                ? portfolioStats.short_balance / closePrice
                : portfolioStats.short_balance
            )
          );
          break;
        case "cover":
          const shortData = portfolioData.short.find(
            ({ symbol }) => symbol === state.symbol
          );
          shortData?.owned &&
            setMaxValue(
              state.purchaseBy === "quantity"
                ? shortData.owned
                : shortData.owned * closePrice
            );
          break;
        default:
      }
      setFinalQuantity(
        Math.floor(
          state.purchaseBy === "quantity"
            ? state.quantity
            : state.quantity / closePrice
        )
      );
      setPrice(closePrice * finalQuantity * commission);
      setPreviousBalance(portfolioStats.total_long_value);
    }
  }, [loading, state]);
  // debounced portfolio allocation
  const [] = useDebounce(
    () => {
      setPortfolioAllocation((100 * price) / (price + previousBalance));
    },
    50,
    [price]
  );

  // handle submit
  const { enqueueSnackbar } = useSnackbar();

  const handleSubmit = () => {
    setSubmitLoading(true);
    axios
      .post(
        `/trade/${state.orderType}/${state.tradeType}?symbol=${state.symbol}&quantity=${state.quantity}`
      )
      .then((response) => {
        console.log(response);
        enqueueSnackbar(`${response.data.result}`, {
          variant: "Success",
        });
      })
      .catch((err) => {
        console.log("err", err);
        enqueueSnackbar(`${err}`, {
          variant: "Error",
        });
      })
      .then(() => setSubmitLoading(false)); //todo send notification
  };

  return (
    <Page>
      <StandardCard>
        <CardContent>
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
              <AutoCompleteTextField
                value={state.symbol}
                setValue={setSymbol}
              />
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
                <ToggleButton
                  value="short"
                  disabled={lockedLoading ? true : locked.level <= 3}
                >
                  Short
                </ToggleButton>
                <ToggleButton
                  value="cover"
                  disabled={lockedLoading ? true : locked.level <= 5}
                >
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

            <Grid item container direction="row" xs={12}>
              <Grid item xs={7} sm={10}>
                <Slider
                  value={state.quantity}
                  onChange={(_event, newValue) => setQuantity(newValue)}
                  getAriaValueText={(t) => `t`}
                  aria-labelledby="discrete-slider"
                  step={1}
                  // marks
                  valueLabelDisplay="on"
                  min={0}
                  max={maxValue}
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
                      {state.purchaseBy === "quantity" ? (
                        <QuantityIcon />
                      ) : (
                        <ValueIcon />
                      )}
                    </InputAdornment>
                  }
                  inputProps={{
                    step: 1,
                    min: 0,
                    max: maxValue,
                    type: "number",
                  }}
                />
              </Grid>
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
            {(state.tradeType === "buy" || state.tradeType === "sell") && (
              <>
                <Grid item xs={12}>
                  Portfolio Allocation:
                </Grid>
                <Grid item xs={12}>
                  <LinearProgress
                    variant="determinate"
                    style={{ height: "20px" }}
                    value={portfolioAllocation}
                  />
                </Grid>
              </>
            )}
          </Grid>
        </CardContent>
      </StandardCard>
      <StandardCard>
        <CardContent>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Order Summary:</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Price per share</TableCell>
                <TableCell align="right">{`$${format(closePrice)}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Shares</TableCell>
                <TableCell align="right">{`${finalQuantity}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Commission</TableCell>
                <TableCell align="right">{`$${format(
                  rawCommission * closePrice * finalQuantity
                )}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <Typography variant="h6">Total</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography variant="h6"> {`$${format(price)}`}</Typography>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
        {submitLoading && <LinearProgress />}
        <CardActions>
          <Button
            onClick={() => setState(defaultState)}
            disabled={submitLoading}
          >
            clear
          </Button>
          <Button onClick={handleSubmit} disabled={submitLoading}>
            Submit
          </Button>
        </CardActions>
      </StandardCard>
    </Page>
  );
};

export default Trading;
