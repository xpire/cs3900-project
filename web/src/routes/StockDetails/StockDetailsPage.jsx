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

import Page from "../../components/page/Page";
import { CenteredCard, StandardCard } from "../../components/common/styled";
import ColoredText, {
  useColoredText,
} from "../../components/common/ColoredText";
import Candlestick from "../../components/graph/Candlestick";
import { Skeleton } from "@material-ui/lab";
import axios from "../../utils/api";
// import ApexCandlestick from "../../components/graph/ApexCandlestick";
import { format } from "../../utils/formatter";
import useHandleSnack from "../../hooks/useHandleSnack";
import TradingHoursIndicator from "../../components/common/TradingHoursIndicator";
import Trade  from  "../../components/trade/TradingPage" 
import Icon from '@material-ui/core/Icon';
import SaveIcon from '@material-ui/icons/Save';
import VisibilityIcon from '@material-ui/icons/Visibility';

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
  const [online, setOnline] = useState(false);
  const [timeSeries, setTimeSeries] = useState(null);
  const [error, setError] = useState(false);
  const { symbol } = useParams();
  let history = useHistory();

  const getRealTimeStockData = () => {
    axios
      .get(`/stocks/real_time?symbols=${symbol}`)
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

  return (
    <Page>
      {!error ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={12} xs={12}>
            <StandardCard style={{position: "relative"}}>
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
                  </Typography> */}
                    {/* Add back when name is here*/}
                    {!loading && (
                      <Grid container spacing={1}>
                        <Grid item>
                          <Chip label={stockData.name} size="small" />
                        </Grid>
                        <Grid item>
                          <Chip label={stockData.exchange} size="small" />
                        </Grid>
                        <Grid item>
                          <TradingHoursIndicator online={online} />
                        </Grid>
                      </Grid>
                    )}
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
                      <Grid item>
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
     

                <Button
                  variant="outlined"
                  color="primary" 
          
                  size="large"
                  startIcon={<VisibilityIcon />}
                  onClick={() => {
                    handleSnack(`/watchlist?symbol=${symbol}`, "post");
                  }}
                  style={{
                    position: "absolute",
                    bottom: "0",
                    padding: "10px",
                    width: "100%"                }}
                >
                  Watch
                </Button>
         
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
          <Grid item xs={6}>
          <StandardCard>
            basic
          </StandardCard>
          </Grid>
          <Grid item xs={6}>
          < Trade symbol={symbol} /> 
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
