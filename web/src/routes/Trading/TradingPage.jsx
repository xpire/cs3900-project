import React, { useState, useEffect } from "react";
import {
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
  TextField,
} from "@material-ui/core";
import QuantityIcon from "@material-ui/icons/LocalAtm";
import ValueIcon from "@material-ui/icons/MonetizationOn";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import { useLocation, useHistory } from "react-router-dom";
import { useDebounce } from "react-use";
import NumberFormat from "react-number-format";
// import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
// import DateFnsUtils from "@date-io/date-fns";

import Page from "../../components/page/Page";
import useApi from "../../hooks/useApi";
import AutoCompleteTextField from "../../components/common/AutoCompleteTextField";
import { format } from "../../utils/formatter";
import { StandardCard } from "../../components/common/styled";
import useHandleSnack from "../../hooks/useHandleSnack";
import TradingHoursIndicator from "../../components/common/TradingHoursIndicator";

function NumberFormatCustom(props) {
  const { inputRef, onChange, maxValue, ...other } = props;
  console.log({ maxValue });
  return (
    <NumberFormat
      {...other}
      getInputRef={inputRef}
      onValueChange={(values) => {
        onChange(values.value);
      }}
      thousandSeparator
      isNumericString
      prefix="$"
      fixedDecimalScale
      allowNegative={false}
      decimalScale={2}
    />
  );
}

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
    quantity: 0,
    limitOrderPrice: 100,
    // date: new Date(),
  };

  const [state, setState] = useState(defaultState);
  const setSymbol = (value) => {
    setState({ ...state, symbol: value });
    history.push(`?symbol=${value}`);
  };
  const setTradeType = (value) =>
    setState({ ...state, tradeType: value, quantity: 0 });
  const setPurchaseBy = (value) =>
    setState({ ...state, purchaseBy: value, quantity: 0 });
  const setQuantity = (value) => setState({ ...state, quantity: value });
  const setOrderType = (value) => setState({ ...state, orderType: value });
  const setLimitOrderPrice = (value) =>
    setState({ ...state, limitOrderPrice: value });
  const [update, setUpdate] = useState(0);

  const handleInputChange = (event) => {
    if (event.target.value === "") {
      setQuantity("");
    } else if (Number(event.target.value) > maxValue) {
      setQuantity(maxValue);
    } else {
      setQuantity(Number(event.target.value));
    }
    setUpdate(update + 1);
  };

  const handleBlur = () => {
    if (state.quantity < 0) {
      setQuantity(0);
    } else if (state.quantity > maxValue) {
      setQuantity(maxValue);
    }
    setUpdate(update + 1);
  };

  // API calls
  const [locked, lockedLoading] = useApi(`/user`, [update]); // check if functionality is locked
  const [portfolioData, portfolioLoading] = useApi(`/portfolio`, [update]); // check owned stock for sell and cover
  const [portfolioStats, portfolioStatsLoading] = useApi(`/portfolio/stats`, [
    update,
  ]); // check overall stats
  const [rawCommission, rawCommissionLoading] = useApi(
    `/stocks/real_time?symbols=${state.symbol}`,
    [
      //check current close price for stock
      state.symbol,
      update,
    ],
    0.005,
    (data) => data[0].commission
  );
  const [closePrice, closePriceLoading] = useApi(
    `/stocks/real_time?symbols=${state.symbol}`,
    [
      //check current close price for stock
      state.symbol,
    ],
    100,
    (data) => data[0].curr_day_close
  );
  const [online, onlineLoading] = useApi(
    `/stocks/real_time?symbols=${state.symbol}`,
    [
      //check current close price for stock
      state.symbol,
    ],
    false,
    (data) => data[0].is_trading
  );

  // state inaccessible to user
  const [maxValue, setMaxValue] = useState(0);
  const [portfolioAllocation, setPortfolioAllocation] = useState(0);
  const [commission, setCommission] = useState(1.005);
  const [price, setPrice] = useState(0);
  const [finalQuantity, setFinalQuantity] = useState(0);
  const [previousBalance, setPreviousBalance] = useState(100);
  const [actualPrice, setActualPrice] = useState(100);

  const loading =
    lockedLoading ||
    portfolioLoading ||
    portfolioStatsLoading ||
    rawCommissionLoading ||
    closePriceLoading ||
    onlineLoading;

  // update state for user input
  useEffect(() => {
    if (!loading) {
      setPreviousBalance(portfolioStats.total_long_value);
      const commissionConst = // for use inside this useeffect (as useState does not run until next rerender)
        state.tradeType === "buy" || state.tradeType === "short"
          ? 1 + rawCommission // buy  and short
          : 1 - rawCommission; // sell and cover
      setCommission(commissionConst);
      const actualPriceConst =
        state.orderType === "limit" ? state.limitOrderPrice : closePrice; // for use inside this useeffect (as useState does not run until next rerender)
      setActualPrice(actualPriceConst);
      switch (state.tradeType) {
        case "buy":
          setMaxValue(
            Math.floor(
              state.purchaseBy === "quantity"
                ? portfolioStats.balance / (actualPriceConst * commissionConst) // take into account commission
                : portfolioStats.balance / commissionConst
            )
          );
          break;
        case "sell":
          const longData = portfolioData.long.find(
            ({ symbol }) => symbol === state.symbol
          );
          longData?.owned
            ? setMaxValue(
                state.purchaseBy === "quantity"
                  ? longData.owned
                  : longData.owned * actualPriceConst
              )
            : setMaxValue(0);

          break;
        case "short":
          setMaxValue(
            Math.floor(
              state.purchaseBy === "quantity"
                ? portfolioStats.short_balance /
                    (actualPriceConst * commissionConst) // take into account commission
                : portfolioStats.short_balance
            )
          );
          break;
        case "cover":
          const shortData = portfolioData.short.find(
            ({ symbol }) => symbol === state.symbol
          );
          shortData?.owned
            ? setMaxValue(
                state.purchaseBy === "quantity"
                  ? shortData.owned
                  : shortData.owned * actualPriceConst
              )
            : setMaxValue(0);

          break;
        default:
      }
      setFinalQuantity(
        Math.floor(
          state.purchaseBy === "quantity"
            ? state.quantity
            : state.quantity / actualPriceConst
        )
      );
    }
  }, [loading, state, update]);
  useEffect(() => setPrice(actualPrice * finalQuantity * commission), [
    actualPrice,
    finalQuantity,
    commission,
  ]);
  // debounced portfolio allocation
  const [] = useDebounce(
    () => {
      setPortfolioAllocation((100 * price) / (price + previousBalance));
      finalQuantity === 0 && setPortfolioAllocation(0); // bug with changing state once not updating portfolio allocation
    },
    50,
    [state, price]
  );

  // handle submit
  const handleSnack = useHandleSnack();

  const handleSubmit = () => {
    setSubmitLoading(true);
    handleSnack(
      `/trade/${state.orderType}/${state.tradeType}?symbol=${
        state.symbol
      }&quantity=${state.quantity}${
        state.orderType === "limit" ? `&limit=${actualPrice}` : ""
      }`,
      "post"
    ).then(() => {
      setSubmitLoading(false);
      setUpdate(update + 1);
      setState(defaultState);
    });
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
              Trading hours:
            </Grid>
            <Grid item xs={9}>
              <TradingHoursIndicator online={online} />
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
                  disabled={lockedLoading ? true : locked.level < 5}
                >
                  Short
                </ToggleButton>
                <ToggleButton
                  value="cover"
                  disabled={lockedLoading ? true : locked.level < 5}
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
                <ToggleButton
                  value="limit"
                  disabled={lockedLoading ? true : locked.level < 3}
                >
                  Limit
                </ToggleButton>
              </ToggleButtonGroup>
            </Grid>
            {state.orderType === "limit" && (
              <>
                <Grid item xs={3}>
                  Limit Price
                </Grid>
                <Grid item xs={9}>
                  <TextField
                    value={state.limitOrderPrice}
                    onChange={setLimitOrderPrice}
                    InputProps={{
                      inputComponent: NumberFormatCustom,
                    }}
                  />
                </Grid>
              </>
            )}
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
                <TableCell />
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Price per share</TableCell>
                <TableCell align="right">{`$${format(actualPrice)}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Shares</TableCell>
                <TableCell align="right">{`${finalQuantity}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Commission</TableCell>
                <TableCell align="right">{`$${format(
                  rawCommission * actualPrice * finalQuantity
                )}`}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <Typography variant="h5">Total</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography variant="h5"> {`$${format(price)}`}</Typography>
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
