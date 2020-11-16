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
  Tooltip,
} from "@material-ui/core";
import QuantityIcon from "@material-ui/icons/LocalAtm";
import ValueIcon from "@material-ui/icons/MonetizationOn";
import { ToggleButton, ToggleButtonGroup } from "@material-ui/lab";
import { useLocation, useHistory } from "react-router-dom";
import { useDebounce } from "react-use";
import NumberFormat from "react-number-format";

import Page from "../../components/page/Page";
import useApi from "../../hooks/useApi";
import AutoCompleteTextField from "../../components/common/AutoCompleteTextField";
import LockedTooltip from "../../components/common/LockedTooltip";
import { format } from "../../utils/formatter";
import { BasicCard, StandardCard } from "../../components/common/styled";
import useHandleSnack from "../../hooks/useHandleSnack";
import TradingHoursIndicator from "../../components/common/TradingHoursIndicator";
import { useDispatch, useSelector } from "react-redux";
import { getStockBySymbol, reloadAll, reloadUser } from "../../reducers";

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
      isAllowed={(values) => {
        console.log({ values });
        return values.floatValue !== 0;
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

const EMPTY_STOCK = {
  symbol: "",
  name: "",
  exchange: "",
  industry: "",
  currency: "",
  type: "",
  curr_day_close: 0.0,
  curr_day_open: 0.0,
  prev_day_close: 0.0,
  commission: 0.0005,
  is_trading: false,
};

const Trading = ({ symbol }) => {
  let history = useHistory();
  const [submitLoading, setSubmitLoading] = useState(false);

  // State accessible to users
  const defaultState = {
    tradeType: "buy",
    purchaseBy: "quantity",
    orderType: "market",
    quantity: 0,
    limitOrderPrice: 100,
    // date: new Date(),
  };

  const [state, setState] = useState(defaultState);
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

  const isUserLoading = useSelector((state) => state.user.is_loading);
  const isStockLoading = useSelector((state) => state.stocks.is_loading);
  const isLoading = (isUserLoading ?? true) || (isStockLoading ?? true);

  let stock = useSelector(getStockBySymbol(symbol));
  stock = isLoading ? EMPTY_STOCK : stock;

  const {
    commission: rawCommission,
    curr_day_close: closePrice,
    is_trading: online,
  } = stock;

  // state inaccessible to user
  const [maxValue, setMaxValue] = useState(0);
  const [portfolioAllocation, setPortfolioAllocation] = useState(0);
  const [commission, setCommission] = useState(1.005);
  const [price, setPrice] = useState(0);
  const [finalQuantity, setFinalQuantity] = useState(0);
  const [previousBalance, setPreviousBalance] = useState(100);
  const [actualPrice, setActualPrice] = useState(100);

  const loading =
    lockedLoading || portfolioLoading || portfolioStatsLoading || isLoading;

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
      let maxValueConst = 0;
      const setMaxValueConst = (val) => {
        maxValueConst = val;
      };
      switch (state.tradeType) {
        case "buy":
          setMaxValueConst(
            Math.floor(
              state.purchaseBy === "quantity"
                ? portfolioStats.balance / (actualPriceConst * commissionConst) // take into account commission
                : portfolioStats.balance / commissionConst
            )
          );
          break;
        case "sell":
          const longData = portfolioData.long.find(
            (elem) => elem.symbol === symbol
          );
          longData?.owned
            ? setMaxValueConst(
                state.purchaseBy === "quantity"
                  ? longData.owned
                  : longData.owned * actualPriceConst
              )
            : setMaxValueConst(0);

          break;
        case "short":
          setMaxValue(
            portfolioStats.short_balance <= 0
              ? 0
              : Math.floor(
                  state.purchaseBy === "quantity"
                    ? portfolioStats.short_balance /
                        (actualPriceConst * commissionConst) // take into account commission
                    : portfolioStats.short_balance
                )
          );
          break;
        case "cover":
          const shortData = portfolioData.short.find(
            (elem) => elem.symbol === symbol
          );
          shortData?.owned
            ? setMaxValueConst(
                state.purchaseBy === "quantity"
                  ? shortData.owned
                  : shortData.owned * actualPriceConst
              )
            : setMaxValueConst(0);

          break;
        default:
      }
      setMaxValue(maxValueConst);

      const finalQuantityConst = Math.floor(
        state.purchaseBy === "quantity"
          ? Math.min(Math.floor(state.quantity))
          : state.quantity / actualPriceConst
      );
      // use limit quantity to maxValueConst
      setFinalQuantity(Math.min(finalQuantityConst, maxValueConst));
      setPrice(actualPriceConst);
    }
  }, [loading, state, update]);
  useEffect(() => setPrice(actualPrice * finalQuantity * commission), [
    actualPrice,
    finalQuantity,
    commission,
    state,
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

  const dispatch = useDispatch();
  const handleSubmit = () => {
    setSubmitLoading(true);
    handleSnack(
      `/trade/${state.orderType}/${
        state.tradeType
      }?symbol=${symbol}&quantity=${finalQuantity}${
        state.orderType === "limit" ? `&limit=${actualPrice}` : ""
      }`,
      "post"
    ).then(() => {
      setSubmitLoading(false);
      setUpdate(update + 1);
      setState(defaultState);
      dispatch(reloadAll);
    });
  };

  return (
    <>
      <BasicCard>
        <CardContent>
          <Grid
            container
            direction="row"
            justify="center"
            alignItems="center"
            spacing={2}
          >
            <Grid item xs={3}>
              Trading Hour:
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
                {!lockedLoading && locked.level >= 5 ? (
                  <ToggleButton value="short">Short</ToggleButton>
                ) : (
                  <LockedTooltip userLevel={locked.level} lockedLevel={5}>
                    <ToggleButton value="short">Short</ToggleButton>
                  </LockedTooltip>
                )}
                {!lockedLoading && locked.level >= 5 ? (
                  <ToggleButton value="cover">Cover</ToggleButton>
                ) : (
                  <LockedTooltip userLevel={locked.level} lockedLevel={5}>
                    <ToggleButton value="cover">Cover</ToggleButton>
                  </LockedTooltip>
                )}
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
              <Grid item xs={7} sm={8}>
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
              <Grid item xs={5} sm={4}>
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
                {!lockedLoading && locked.level >= 3 ? (
                  <ToggleButton value="limit">Limit</ToggleButton>
                ) : (
                  <LockedTooltip userLevel={locked.level} lockedLevel={3}>
                    <ToggleButton value="limit">Limit</ToggleButton>
                  </LockedTooltip>
                )}
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
            {state.tradeType === "buy" && (
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
      </BasicCard>
      <BasicCard>
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
                <Tooltip title="This is a rough estimate. Actual value traded may be different.">
                  <TableCell>
                    <Typography variant="h5">Total*</Typography>
                  </TableCell>
                </Tooltip>
                <Tooltip title="This is a rough estimate. Actual value traded may be different.">
                  <TableCell align="right">
                    <Typography variant="h5"> {`$${format(price)}`}</Typography>
                  </TableCell>
                </Tooltip>
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
      </BasicCard>
    </>
  );
};

export default Trading;
