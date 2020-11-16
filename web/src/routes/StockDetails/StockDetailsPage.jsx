import React, { useEffect, useState } from "react";
import {
  Typography,
  Chip,
  CardContent,
  CardActions,
  Grid,
  Menu,
  MenuItem,
  IconButton,
  Button,
  CircularProgress,
  Tooltip,
  CardHeader,
  ListItemText,
  ListItemSecondaryAction,
  Switch,
  Tabs,
  Tab,
} from "@material-ui/core";
import { FormatListNumberedOutlined, MoreVert } from "@material-ui/icons";
import { Link, useParams } from "react-router-dom";
import List from "@material-ui/core/List";
import { useSelector, useDispatch } from "react-redux";
import styled from "styled-components";

import Page from "../../components/page/Page";
import { CenteredCard, StandardCard } from "../../components/common/styled";
import LockedTooltip from "../../components/common/LockedTooltip";
import ColoredText, {
  useColoredText,
} from "../../components/common/ColoredText";
import Candlestick from "../../components/graph/Candlestick";
import { Skeleton } from "@material-ui/lab";
import axios from "../../utils/api";
import { format } from "../../utils/formatter";
import useHandleSnack from "../../hooks/useHandleSnack";
import Trade from "../../components/trade/TradingPage";
import { BasicCard } from "../../components/common/styled";
import PortfolioPolar from "../../components/graph/PortfolioPolar";
import StockDisplayTable from "../../components/common/StockDisplayTable";
import SortableStockTable, {
  tableTypes,
  RenderItem,
} from "../../components/common/SortableStockTable";
import {
  getOrdersForSymbol,
  getTransactionsForSymbol,
  removeFromOrdersWithSnack,
} from "../../reducers/index";

const orderColumns = [
  {
    field: "symbol",
    title: (
      <RenderItem title="Symbol" subtitle="Timestamp" alignItems="flex-start" />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.timestamp}
        subtitleType={tableTypes.DATE}
        alignItems="flex-start"
      />
    ),
    align: "right",
  },
  {
    field: "trade_type",
    title: <RenderItem title="Trade Type" subtitle="Quantity" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.trade_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.qty}
        subtitleType={tableTypes.SHARES}
      />
    ),
    align: "right",
  },
  {
    field: "order_type",
    title: <RenderItem title="Order Type" subtitle="(Limit Price)" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.order_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.order_type === "LIMIT" ? rowData.limit_price : ""}
        subtitleType={
          rowData.order_type === "LIMIT" ? tableTypes.CURRENCY : tableTypes.TEXT
        }
      />
    ),
    align: "right",
  },
];

const columns = [
  {
    field: "symbol",
    title: (
      <RenderItem title="Symbol" subtitle="Status" alignItems="flex-start" />
    ),
    render: (rowData) => (
      <RenderItem
        title={rowData.symbol}
        titleType={tableTypes.TEXT}
        subtitle={rowData.is_cancelled ? "Cancelled" : "Executed"}
        subtitleType={tableTypes.TEXT}
        alignItems="flex-start"
      />
    ),
  },
  {
    field: "trade_type",
    title: <RenderItem title="Trade Type" subtitle="Quantity" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.trade_type}
        titleType={tableTypes.TEXT}
        subtitle={rowData.qty}
        subtitleType={tableTypes.NUMBER}
      />
    ),
    align: "right",
  },
];

const transactionColumns = [
  ...columns,
  {
    field: "price",
    title: <RenderItem title="Execution Price" subtitle="Value" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.is_cancelled === true ? "Cancelled" : rowData.price}
        titleType={
          rowData.is_cancelled === true ? tableTypes.TEXT : tableTypes.CURRENCY
        }
        subtitle={rowData.is_cancelled === true ? undefined : rowData.value}
        subtitleType={
          rowData.is_cancelled === true ? undefined : tableTypes.CURRENCY
        }
      />
    ),
    align: "right",
  },
];

const options = [
  { key: "leftEdge", name: "Left Edge", level: 0 },
  { key: "rightEdge", name: "Right Edge", level: 0 },
  { key: "showVolume", name: "Volumes", level: 2 },
  { key: "showEma20", name: "EMA", level: 7 },
  { key: "showBollingerSeries", name: "BB", level: 9 },
];

const StyledMenuItem = styled(MenuItem)`
  width: 200px;
`;

const CandleStickWithState = ({ timeSeries }) => {
  const [state, setState] = useState({
    leftEdge: true,
    rightEdge: true,
    showVolume: false,
    showEma20: false,
    showBollingerSeries: false,
  });

  const handleToggle = (key) => () => {
    setState({ ...state, [key]: !state[key] });
  };

  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const userLevel = useSelector((state) => state.user.basic.level);

  return (
    <StandardCard>
      <Grid container direction="row-reverse">
        <Grid item>
          <IconButton
            aria-controls="simple-menu"
            aria-haspopup="true"
            onClick={handleClick}
          >
            <MoreVert />
          </IconButton>
        </Grid>
      </Grid>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {options.map(({ name, key, level }) => {
          const disabled = !!userLevel && userLevel < level;
          return (
            <LockedTooltip userLevel={userLevel} lockedLevel={level} key={key}>
              <StyledMenuItem
                onClick={!disabled ? handleToggle(key) : undefined}
              >
                <ListItemText color="textSecondary">{name}</ListItemText>
                <ListItemSecondaryAction>
                  <Switch
                    edge="end"
                    checked={state[key]}
                    onChange={!disabled ? handleToggle(key) : undefined}
                    disabled={disabled}
                  />
                </ListItemSecondaryAction>
              </StyledMenuItem>
            </LockedTooltip>
          );
        })}
      </Menu>
      <CardContent>
        <div // fix scrolling body in chrome
          onMouseEnter={() => {
            document.addEventListener("wheel", preventDefault, {
              passive: false,
            });
          }}
          onMouseLeave={() => {
            document.removeEventListener("wheel", preventDefault, false);
          }}
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
          }}
        >
          {timeSeries === null ? (
            <CircularProgress color="primary" size={50} />
          ) : (
            <Candlestick data={timeSeries} type="hybrid" {...state} />
          )}
        </div>
      </CardContent>
    </StandardCard>
  );
};

// prevent default behaviour for scroll event
const preventDefault = (e) => {
  e = e || window.event;
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.returnValue = false;
};

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

const StockDetails = () => {
  const { symbol } = useParams();

  // TIME SERIES DATA
  const [timeSeries, setTimeSeries] = useState(null);
  const [error, setError] = useState(false);
  const pollStockData = () => {
    axios
      .get(`/stocks/time_series?symbol=${symbol}&days=3650`)
      .then((response) => {
        let data = response.data;
        data = data
          .map(({ date, open, close, high, low, volume }) => {
            return {
              date: new Date(date),
              open: +open,
              high: +high,
              low: +low,
              close: +close,
              volume: +volume,
            };
          })
          .reverse();
        setTimeSeries(data);
      })
      .catch((err) => setError(true));
  };
  useEffect(pollStockData, []);

  // STOCK DATA
  const isLoading = useSelector((state) => state.stocks.is_loading);
  let stock = useSelector((state) => state.stocks.dict[symbol]);
  if (!stock) {
    stock = EMPTY_STOCK;
  }
  const stockData = isLoading ? { skeleton: true } : stock;
  const latestPrice = isLoading ? 0 : stockData.curr_day_close;
  const dayGain = isLoading
    ? 0
    : (100 * (stockData.curr_day_close - stockData.prev_day_close)) /
      stockData.prev_day_close;

  // NAME TRUNCATION
  const MAX_NAME_LENGTH = 20;
  const truncateName = stock.name.length > MAX_NAME_LENGTH;
  const truncatedName =
    stock.name.substring(0, MAX_NAME_LENGTH) + (truncateName ? "..." : "");

  // TAB
  const [tab, setTab] = useState(0);

  const dispatch = useDispatch();
  const handleSnack = useHandleSnack();

  const transHist = useSelector(getTransactionsForSymbol(symbol));
  const ordersHist = useSelector(getOrdersForSymbol(symbol));
  const [delta] = useColoredText(latestPrice);

  return (
    <Page>
      {!error ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item lg={3} md={4} sm={12} xs={12}>
            {/* STOCK BASIC DETAILS */}
            <StandardCard style={{ position: "relative" }}>
              <CardContent>
                <Grid
                  direction="row"
                  container
                  justify="space-between"
                  alignItems="flex-end"
                >
                  <Grid item md={12} sm={6}>
                    <Typography variant="h2">{symbol}</Typography>
                    <Grid>
                      <List dense={true}>
                        <StockDisplayTable
                          name={truncatedName}
                          exchange={stockData.exchange}
                          industry={stockData.industry}
                          currency={stockData.currency}
                          type={stockData.type}
                          fullname={stockData.name}
                          renderStatus={!truncateName}
                        />
                      </List>
                    </Grid>
                  </Grid>
                  <Grid item md={12} sm={6}>
                    <Grid item container direction="row" justify="flex-end">
                      <Grid item>
                        <ColoredText
                          color={dayGain > 0 ? "green" : "red"}
                          variant="h2"
                          align="right"
                          delta={delta}
                        >
                          {isLoading ? <Skeleton /> : `${format(dayGain)}%`}
                        </ColoredText>
                      </Grid>
                    </Grid>
                    <Grid item container direction="row" justify="flex-end">
                      <Grid item>
                        <ColoredText
                          color={dayGain > 0 ? "green" : "red"}
                          variant="h3"
                          align="right"
                          delta={delta}
                        >
                          {isLoading ? <Skeleton /> : `$${format(latestPrice)}`}
                        </ColoredText>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </CardContent>
            </StandardCard>
          </Grid>
          {/* STOCK CANDLE STICK GRAPH */}
          <Grid item lg={9} md={8} sm={12} xs={12}>
            <CandleStickWithState timeSeries={timeSeries} />
          </Grid>
          {/* ORDERS AND RANSACTION HISTORY */}
          <Grid item md={6} sm={12} xs={12}>
            <BasicCard>
              <Grid item xs={12}>
                <Tabs
                  value={tab}
                  onChange={(_event, newValue) => {
                    setTab(newValue);
                  }}
                  indicatorColor="primary"
                  textColor="primary"
                  variant="fullWidth"
                >
                  <Tab label="Orders" />
                  <Tab label="Transaction History" />
                </Tabs>
              </Grid>
              {tab === 0 ? (
                <SortableStockTable
                  title="Orders"
                  columns={orderColumns}
                  data={ordersHist}
                  handleDelete={({ id }) =>
                    dispatch(removeFromOrdersWithSnack(id, handleSnack))
                  }
                  buttons={false}
                  key={"SortableStockTable-Orders"}
                />
              ) : (
                <SortableStockTable
                  title="History"
                  columns={transactionColumns}
                  data={transHist}
                  buttons={false}
                  key={"SortableStockTable-History"}
                />
              )}
            </BasicCard>
          </Grid>

          {/* STOCK TRADE PANEL */}
          <Grid item md={6} sm={12} xs={12}>
            <Trade symbol={symbol} />
          </Grid>
        </Grid>
      ) : (
        <CenteredCard>
          {/* STOCK NOT FOUND*/}
          <CardContent>
            <Typography variant="h2">
              Sorry, we can't find this stock's information...
            </Typography>
            <Typography>
              Either the symbol "{symbol}" is not real or it is not currently
              supported.
            </Typography>
          </CardContent>
          <CardActions>
            <Button
              variant="contained"
              color="primary"
              style={{ marginTop: "20px" }}
              component={Link}
              to="/market"
            >
              Go back
            </Button>
          </CardActions>
        </CenteredCard>
      )}
    </Page>
  );
};

export default StockDetails;
