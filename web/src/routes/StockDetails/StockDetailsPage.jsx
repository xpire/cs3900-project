import React, { useEffect, useState } from "react";
import {
  Typography,
  Chip,
  CardContent,
  CardActions,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Button,
  CircularProgress,
  Tooltip,
} from "@material-ui/core";
import { Link, useParams, useHistory } from "react-router-dom";
import List from "@material-ui/core/List";

import Page from "../../components/page/Page";
import { CenteredCard, StandardCard } from "../../components/common/styled";
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
import SortableTable, {
  tableTypes,
} from "../../components/common/SortableTable";
import SortableStockTable, {
  RenderItem,
} from "../../components/common/SortableStockTable";

function createData(name, value) {
  return { name, value };
}

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

const rows = [
  createData("Previous Close", 1594.0),
  createData("Open", 2374.3),
  createData("Day's Range", 2626.0),
  createData("52 Week's Range", 3054.3),
  createData("Start Date", 3563.9),
  createData("Market Cap", 3563.9),
  createData("Volume", 3563.9),
  createData("Volume (24hr)", 3563.9),
  createData("EPS", 3563.9),
  createData("PE", 35649.9),
];

const headCells = [
  // {
  //   id: "timestamp",
  //   formatType: tableTypes.TEXT,
  //   disablePadding: false,
  //   label: "TimeStamp",
  //   color: true,
  // },
  {
    id: "symbol",
    formatType: tableTypes.TEXT,
    disablePadding: true,
    label: "Symbol",
  },
  // {
  //   id: "name",
  //   formatType: tableTypes.TEXT,
  //   disablePadding: false,
  //   label: "Name",
  // },
  {
    id: "order_type",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Order Type",
  },
  {
    id: "trade_type",
    formatType: tableTypes.TEXT,
    disablePadding: false,
    label: "Trade Type",
  },
  {
    id: "price",
    formatType: tableTypes.CURRENCY,
    disablePadding: false,
    label: "Price",
  },
  {
    id: "qty",
    formatType: tableTypes.NUMBER,
    disablePadding: false,
    label: "Quantity",
  },
  {
    id: "is_cancelled",
    formatType: tableTypes.TEXT,
    disablePadding: true,
    label: "Status",
    // color: true,
  },
];

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
  let history = useHistory();
  const [norm, setTableNorm] = useState([]);
  const [transHist, setTransHist] = useState([]);
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

  const getHistTrans = async () => {
    await axios.get("/transactions").then((response) => {
      const data = response.data;
      setTransHist(
        data
          .filter((elem) => elem.symbol === symbol)
          .map(
            ({
              is_cancelled,
              name,
              order_type,
              price,
              qty,
              symbol,
              timestamp,
              trade_type,
              value,
            }) => {
              return {
                is_cancelled: is_cancelled ? "cancelled" : "active",
                order_type: order_type,
                price: price.toFixed(2),
                qty: qty,
                symbol: symbol,
                timestamp: timestamp,
                trade_type: trade_type,
                value: value,
              };
            }
          )
      );
    });
  };

  useEffect(() => {
    getRealTimeStockData();
    getCurrentPortfolio();
    getHistTrans();
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
            <StandardCard>
              <CardContent>
                <div // fix scrolling body in chrome
                  onMouseEnter={() => {
                    document.addEventListener("wheel", preventDefault, {
                      passive: false,
                    });
                  }}
                  onMouseLeave={() => {
                    document.removeEventListener(
                      "wheel",
                      preventDefault,
                      false
                    );
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
                    <Candlestick
                      data={timeSeries}
                      type="hybrid"
                      leftEdge={left}
                    />
                  )}
                </div>
              </CardContent>
            </StandardCard>
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
                    {/* <SortableTable
                      data={transHist}
                      header={headCells}
                      title="History"
                      buttons={false}
                      handleDelete={null}
                      handleRefresh={null}
                      toolbar={false}
                    /> */}
                  </Grid>
                </Grid>
              </CardContent>
              <SortableStockTable
                title="History"
                columns={columns}
                data={transHist}
                // isLoading={transactionDataLoading}
              />
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
