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
} from "@material-ui/core";
import { Link, useParams, useHistory } from "react-router-dom";
import { useSnackbar } from "notistack";

import Page from "../../components/page/Page";
import {
  ColoredText,
  CenteredCard,
  StandardCard,
} from "../../components/common/styled";
import Candlestick from "../../components/graph/Candlestick";
import { Skeleton } from "@material-ui/lab";
import axios from "../../utils/api";
// import ApexCandlestick from "../../components/graph/ApexCandlestick";

function createData(name, value) {
  return { name, value };
}

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

// prevent default behaviour for scroll event
const preventDefault = (e) => {
  e = e || window.event;
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.returnValue = false;
};

const TableInfo = ({ rows }) => (
  <TableContainer>
    <Table>
      <TableBody>
        {rows.map((row) => (
          <TableRow key={row.name}>
            <TableCell component="th" scope="row">
              {row.name}
            </TableCell>
            <TableCell align="right">{row.value}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);

const StockDetails = () => {
  // grab the list of available stocks
  // const stockCode = props.match.params.symbol.toUpperCase();
  const [stockData, setStockData] = useState({ skeleton: true });
  const [latestPrice, setLatestPrice] = useState(0);
  const [dayGain, setDayGain] = useState(0);
  const [loading, setLoading] = useState(true);
  const [timeSeries, setTimeSeries] = useState(null);
  const [error, setError] = useState(false);
  const { symbol } = useParams();
  let history = useHistory();
  const { enqueueSnackbar } = useSnackbar();

  const getRealTimeStockData = () => {
    axios
      .get(`/stocks/stocks?symbols=${symbol}`)
      .then((response) => {
        const data = response.data;
        setStockData(data[0]);
        setLoading(false);
      })
      .catch((err) => setError(true));
  };

  useEffect(() => {
    getRealTimeStockData();
    const interval = setInterval(getRealTimeStockData, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if ("curr_close_price" in stockData) {
      setLatestPrice(stockData.curr_close_price);
      let gain =
        (100 * (stockData.curr_close_price - stockData.prev_close_price)) /
        stockData.prev_close_price;
      setDayGain(gain);
    }
  }, [stockData]);

  const pollStockData = () => {
    axios
      .get(`/stocks/time_series?symbol=${symbol}&days=90`)
      .then((response) => {
        let data = response.data;
        data = data
          .map(({ datetime, open, close, high, low, volume }) => {
            return {
              date: new Date(datetime),
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

  return (
    <Page>
      {!error ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={12} xs={12}>
            <StandardCard>
              <CardContent>
                <Grid
                  direction="row"
                  container
                  justify="space-between"
                  alignItems="flex-end"
                >
                  <Grid item md={12} sm={6}>
                    <Typography variant="h2">{symbol}</Typography>
                    {/* <Typography variant="h4"> 
                    {loading ? <Skeleton /> : stockData.name}
                  </Typography> */}{" "}
                    {/* Add back when name is here*/}
                    {!loading && <Chip label={stockData.name} size="small" />}
                    {!loading && (
                      <Chip label={stockData.exchange} size="small" />
                    )}
                  </Grid>
                  <Grid item md={12} sm={6}>
                    <Grid item>
                      <ColoredText
                        color={dayGain > 0 ? "green" : "red"}
                        variant="h2"
                        align="right"
                      >
                        {loading ? <Skeleton /> : `${dayGain?.toFixed(2)}%`}
                      </ColoredText>
                    </Grid>
                    <Grid item>
                      <ColoredText
                        color={dayGain > 0 ? "green" : "red"}
                        variant="h3"
                        align="right"
                      >
                        {loading ? <Skeleton /> : `$${latestPrice?.toFixed(2)}`}
                      </ColoredText>
                    </Grid>
                  </Grid>
                </Grid>
              </CardContent>
              <CardActions>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => {
                    axios
                      .post(`/watchlist?symbol=${symbol}`)
                      .then((response) => {
                        console.log({ response });
                        response.data?.result === "success"
                          ? enqueueSnackbar(
                              `${response.data.result}! ${symbol} added to watchlist`,
                              {
                                variant: "Success",
                              }
                            )
                          : enqueueSnackbar(`${response.data.result}`, {
                              variant: "Warning",
                            });
                        console.log({ response });
                        console.log(response.data.result === "success");
                      })
                      .catch((err) =>
                        enqueueSnackbar(`${err}`, {
                          variant: "Error",
                        })
                      );
                  }}
                >
                  Watch
                </Button>

                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => history.push(`/trading?symbol=${symbol}`)}
                >
                  Trade
                </Button>
              </CardActions>
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
                    <Candlestick data={timeSeries} type="hybrid" />
                  )}
                </div>
              </CardContent>
            </StandardCard>
          </Grid>
          <Grid item xs={12}>
            <StandardCard>
              <CardContent>
                <Typography variant="h5">Further Information</Typography>

                <Grid container direction="row">
                  <Grid item sm={6} xs={12}>
                    <TableInfo
                      rows={rows.slice(0, Math.floor(rows.length / 2))}
                    />
                  </Grid>
                  <Grid item sm={6} xs={12}>
                    <TableInfo rows={rows.slice(Math.floor(rows.length / 2))} />
                  </Grid>
                </Grid>
              </CardContent>
            </StandardCard>
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
