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
import { MoreVert } from "@material-ui/icons";
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
import { tableTypes } from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";
import { removeFromOrdersWithSnack } from "../../reducers/index";

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
        subtitle={rowData.is_cancelled}
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
  // {
  //   field: "price",
  //   title: <RenderItem title="Price" subtitle="Value" />,
  //   render: (rowData) => (
  //     <RenderItem
  //       title={rowData.price}
  //       titleType={tableTypes.CURRENCY}
  //       subtitle={rowData.value}
  //       subtitleType={tableTypes.CURRENCY}
  //     />
  //   ),
  //   align: "right",
  // },
];

const orderColumns = [
  ...columns,
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

const transactionColumns = [
  ...columns,
  {
    field: "price",
    title: <RenderItem title="Price" subtitle="Value" />,
    render: (rowData) => (
      <RenderItem
        title={rowData.price}
        titleType={tableTypes.CURRENCY}
        subtitle={rowData.value}
        subtitleType={tableTypes.CURRENCY}
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
          const disabled = !!userLevel && userLevel <= level;
          return (
            <LockedTooltip userLevel={userLevel} lockedLevel={level}>
              <StyledMenuItem onClick={!disabled && handleToggle(key)}>
                <ListItemText color="textSecondary">{name}</ListItemText>
                <ListItemSecondaryAction>
                  <Switch
                    edge="end"
                    checked={state[key]}
                    onChange={!disabled && handleToggle(key)}
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
          {/* <ApexCandlestick data={parsedApexData} /> */}
          {timeSeries === null ? (
            <CircularProgress color="primary" size={50} />
          ) : (
            <Candlestick data={timeSeries} type="hybrid" {...state} />
            // <Candlestick data={timeSeries} type="hybrid" />
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

const StockDetails = () => {
  // grab the list of available stocks
  // const stockCode = props.match.params.symbol.toUpperCase();
  const [stockData, setStockData] = useState({ skeleton: true });
  const [latestPrice, setLatestPrice] = useState(0);
  const [dayGain, setDayGain] = useState(0);
  const [loading, setLoading] = useState(true);
  const [online, setOnline] = useState(false);
  const [timeSeries, setTimeSeries] = useState(null);
  const [error, setError] = useState(false);
  const { symbol } = useParams();
  const [norm, setTableNorm] = useState([]);
  // const [transHist, setTransHist] = useState([]);
  const [portfolio, setPortfolio] = useState({
    long: [],
    short: [],
  });

  const L = 15;
  const getRealTimeStockData = async () => {
    await axios
      .get(`/stocks/real_time?symbols=${symbol}`)
      .then((response) => {
        const data = response.data;
        const norm = data[0].name.length < L;
        const ttname = data[0].name;

        if (norm) {
          data[0].fullname = "placeholder";
        } else {
          data[0].fullname = data[0].name; // Now name is abbrev
          data[0].name = data[0].name.substring(0, L) + "...";
        }

        // console.log(data[0].fullname)
        setStockData(data[0]);
        setTableNorm([norm, ttname]);
        setLoading(false);
      })
      .catch((err) => setError(true));
  };

  const getCurrentPortfolio = async () => {
    await axios.get("/portfolio").then((response) => {
      const data = response.data;
      console.log(data);
      setPortfolio({
        long: data.long.map((item) => [
          `${item.symbol}: ${item.owned}`,
          Number(item.total_paid.toFixed(2)),
        ]),
        short: data.short.map((item) => [
          `${item.symbol}: ${item.owned}`,
          Number(item.total_paid.toFixed(2)),
        ]),
      });
    });
  };
  const [tab, setTab] = useState(0);
  const dispatch = useDispatch();

  const transHist = useSelector((state) => state.user.transactions);
  const ordersHist = useSelector((state) => state.user.orders);

  // const getHistTrans = async () => {
  //   await axios.get("/transactions").then((response) => {
  //     const data = response.data;
  //     setTransHist(
  //       data
  //         .filter((elem) => elem.symbol === symbol)
  //         .map(
  //           ({
  //             is_cancelled,
  //             name,
  //             order_type,
  //             price,
  //             qty,
  //             symbol,
  //             timestamp,
  //             trade_type,
  //             value,
  //           }) => {
  //             return {
  //               is_cancelled: is_cancelled ? "cancelled" : "active",
  //               order_type: order_type,
  //               price: price.toFixed(2),
  //               qty: qty,
  //               symbol: symbol,
  //               timestamp: timestamp,
  //               trade_type: trade_type,
  //               value: value,
  //             };
  //           }
  //         )
  //         ?.reverse()
  //     );
  //   });
  // };

  useEffect(() => {
    getRealTimeStockData();
    getCurrentPortfolio();
    // getHistTrans();
    const interval = setInterval(getRealTimeStockData, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if ("curr_day_close" in stockData) {
      setLatestPrice(stockData.curr_day_close);
      let gain =
        (100 * (stockData.curr_day_close - stockData.prev_day_close)) /
        stockData.prev_day_close;
      setDayGain(gain);
      setOnline(stockData.is_trading);
    }
  }, [stockData]);

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

  const handleSnack = useHandleSnack();

  const [delta] = useColoredText(latestPrice);

  const [left, setLeft] = useState(true);
  const [margin, setMargin] = useState({
    left: 70,
    right: 70,
    top: 20,
    bottom: 30,
  });

  return (
    <Page>
      {!error ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={12} xs={12}>
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
                          name={stockData.name}
                          exchange={stockData.exchange}
                          industry={stockData.industry}
                          currency={stockData.currency}
                          type={stockData.type}
                          fullname={norm[1]}
                          renderStatus={norm[0]}
                        />
                      </List>
                    </Grid>
                  </Grid>
                  <Grid item md={12} sm={6}>
                    <Grid item container direction="row-reverse">
                      <Grid item>
                        <ColoredText
                          color={dayGain > 0 ? "green" : "red"}
                          variant="h2"
                          align="right"
                          delta={delta}
                        >
                          {loading ? <Skeleton /> : `${format(dayGain)}%`}
                        </ColoredText>
                      </Grid>
                    </Grid>
                    <Grid item container direction="row-reverse">
                      <Grid item xs>
                        <ColoredText
                          color={dayGain > 0 ? "green" : "red"}
                          variant="h3"
                          align="right"
                          delta={delta}
                        >
                          {loading ? <Skeleton /> : `$${format(latestPrice)}`}
                        </ColoredText>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </CardContent>
            </StandardCard>
          </Grid>
          <Grid item md={9} sm={12} xs={12}>
            <CandleStickWithState timeSeries={timeSeries} />
          </Grid>
          <Grid item md={6} sm={12} xs={12}>
            <BasicCard sty>
              <CardContent>
                <Grid item container direction="row">
                  <Grid item xs={12} sm={6}>
                    <Typography variant="h5">Long</Typography>
                    <PortfolioPolar data={portfolio["long"]} />
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Typography variant="h5">Short</Typography>
                    <PortfolioPolar data={portfolio["short"]} />
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="h5">Transaction History</Typography>
                  </Grid>
                </Grid>
              </CardContent>
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
                  <Tab label="Transaction History" />
                  <Tab label="Orders" />
                </Tabs>
              </Grid>
              {tab === 0 ? (
                <SortableStockTable
                  title="History"
                  columns={orderColumns}
                  data={transHist}
                  handleDelete={({ id }) =>
                    dispatch(removeFromOrdersWithSnack(id, handleSnack))
                  }
                />
              ) : (
                <SortableStockTable
                  title="Orders"
                  columns={transactionColumns}
                  data={ordersHist}
                />
              )}
            </BasicCard>
          </Grid>

          <Grid item md={6} sm={12} xs={12}>
            <Trade symbol={symbol} />
          </Grid>
        </Grid>
      ) : (
        <CenteredCard>
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
