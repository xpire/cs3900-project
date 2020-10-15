import React, { useEffect, useState } from "react";
import {
  Typography,
  Chip,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Button,
  CardActions,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { Link, useParams } from "react-router-dom";

// import { AuthContext } from "../utils/authentication";
import Page from "../../components/page/Page";
import {
  ColoredText,
  CenteredCard,
  StandardCard,
} from "../../components/common/styled";
import Candlestick from "../../components/graph/Candlestick";
// import ApexCandlestick from "../../components/graph/ApexCandlestick";

// import * as stockData from "../../utils/stocksList.json"; //TODO: make this an API call
import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call

// const listData = stockData.data.map(({ symbol }) => symbol);

const parsedData = TimeSeriesData.AAPL.values
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

// const parsedApexData = TimeSeriesData.AAPL.values.map(
//   ({ datetime, open, close, high, low }) => {
//     return { x: new Date(datetime), y: [open, high, low, close] };
//   }
// );

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
  const [error, setError] = useState(false);
  const { symbol } = useParams();

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/stocks?symbols=${symbol}`)
      .then((response) => response.json())
      .then((data) => {
        setStockData(data[0]);
        console.log(data[0]);
      })
      .catch(() => setError(true));
  }, []);

  return (
    <Page style={{ padding: "20px" }}>
      {!error ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={12} xs={12}>
            <StandardCard>
              <Grid
                direction="row"
                container
                justify="space-between"
                alignItems="flex-end"
              >
                <Grid item md={12} sm={6}>
                  <Typography variant="h2">{symbol}</Typography>
                  <Typography variant="h4">{stockData.name}</Typography>
                  <Chip label={stockData.exchange} size="small" />
                </Grid>
                <Grid item md={12} sm={6}>
                  <Grid item>
                    <ColoredText
                      color={stockData.day_gain > 0 ? "green" : "red"}
                      variant="h2"
                      align="right"
                    >
                      {stockData.day_gain?.toFixed(1)}%
                    </ColoredText>
                  </Grid>
                  <Grid item>
                    <ColoredText
                      color={stockData.day_gain > 0 ? "green" : "red"}
                      variant="h3"
                      align="right"
                    >
                      ${stockData.latest_price?.toFixed(2)}
                    </ColoredText>
                  </Grid>
                  <Grid container direction="row-reverse" spacing={2}>
                    <Grid item>
                      <Button variant="outlined" color="primary">
                        Watch
                      </Button>
                    </Grid>
                    <Grid item>
                      <Button variant="outlined" color="primary">
                        Trade
                      </Button>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </StandardCard>
          </Grid>
          <Grid item md={9} sm={12} xs={12}>
            <StandardCard>
              <div // fix scrolling body in chrome
                onMouseEnter={() => {
                  document.addEventListener("wheel", preventDefault, {
                    passive: false,
                  });
                }}
                onMouseLeave={() => {
                  document.removeEventListener("wheel", preventDefault, false);
                }}
              >
                {/* <ApexCandlestick data={parsedApexData} /> */}
                <Candlestick data={parsedData} type="hybrid" />
              </div>
            </StandardCard>
          </Grid>
          <Grid item xs={12}>
            <StandardCard>
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
            </StandardCard>
          </Grid>
        </Grid>
      ) : (
        <CenteredCard>
          <Typography variant="h2">
            Sorry, we can't find this stock's information...
          </Typography>
          <Typography>
            Either the symbol "{symbol}" is not real or it is not currently
            supported.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            style={{ marginTop: "20px" }}
            component={Link}
            to="/market"
          >
            Go back
          </Button>
        </CenteredCard>
      )}
    </Page>
  );
};

export default StockDetails;
