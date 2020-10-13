import React from "react";
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

import * as stockData from "../../utils/stocksList.json"; //TODO: make this an API call
import * as TimeSeriesData from "../../utils/stocksTimeSeries.json"; //TODO: make this an API call

const listData = stockData.data.map(({ symbol }) => symbol);

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
  const { symbol } = useParams();
  const myStockData = stockData.data.find(
    (s) => s.symbol.toUpperCase() === symbol.toUpperCase()
  );
  return (
    <Page style={{ padding: "20px" }}>
      {listData.includes(symbol) ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={5} xs={12}>
            <StandardCard>
              <Grid direction="row" container alignItems="flex-end">
                <Grid item sm={12} xs={6}>
                  <Typography variant="h2">{symbol}</Typography>
                  <Typography variant="h4">{myStockData.name}</Typography>
                  <Chip label={myStockData.type} size="small" />
                </Grid>
                <Grid item sm={12} xs={6}>
                  <ColoredText color="green" variant="h2">
                    +20%
                  </ColoredText>
                  <CardActions>
                    <Button variant="outlined" color="primary">
                      Watch
                    </Button>
                    <Button variant="outlined" color="primary">
                      Trade
                    </Button>
                  </CardActions>
                </Grid>
              </Grid>
            </StandardCard>
          </Grid>
          <Grid item md={9} sm={7} xs={12}>
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
