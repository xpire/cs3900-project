import React from "react";
import {
  Typography,
  Chip,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
} from "@material-ui/core";
import { Link } from "react-router-dom";

// import { AuthContext } from "../utils/authentication";
import Page from "../components/page/Page";
import {
  ColoredText,
  CenteredCard,
  StandardCard,
} from "../components/common/styled";
import Candlestick from "../components/graph/Candlestick";
// import ApexCandlestick from "../components/graph/ApexCandlestick";

import * as stockData from "../utils/stocksList.json"; //TODO: make this an API call
import * as TimeSeriesData from "../utils/stocksTimeSeries.json"; //TODO: make this an API call

const listData = stockData.data.map(({ symbol }) => symbol);

const parsedData = TimeSeriesData.AAPL.values
  .map(({ datetime, open, close, high, low }) => {
    return {
      date: new Date(datetime),
      open: +open,
      high: +high,
      low: +low,
      close: +close,
    };
  })
  .reverse();

function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData("Frozen yoghurt", 159, 6.0, 24, 4.0),
  createData("Ice cream sandwich", 237, 9.0, 37, 4.3),
  createData("Eclair", 262, 16.0, 24, 6.0),
  createData("Cupcake", 305, 3.7, 67, 4.3),
  createData("Gingerbread", 356, 16.0, 49, 3.9),
];

// prevent default behaviour for scroll event
const preventDefault = (e) => {
  e = e || window.event;
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.returnValue = false;
};

const StockDetails = (props) => {
  // grab the list of available stocks
  const stockCode = props.match.params.symbol.toUpperCase();
  const myStockData = stockData.data.find(
    ({ symbol }) => symbol.toUpperCase() === stockCode
  );
  const [currentData, setCurrentData] = React.useState(parsedData);
  return (
    <Page style={{ padding: "20px" }}>
      {listData.includes(stockCode) ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={5} xs={12}>
            <StandardCard>
              <Typography variant="h1">{stockCode}</Typography>
              <Typography variant="h4">{myStockData.name}</Typography>
              <Chip label={myStockData.type} />
              <ColoredText color="green" variant="h2">
                +20%
              </ColoredText>
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
                <Candlestick data={currentData} type="hybrid" />
              </div>
            </StandardCard>
          </Grid>
          <Grid item xs={12}>
            <StandardCard>
              <Typography variant="h3">Hello guys</Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Dessert (100g serving)</TableCell>
                      <TableCell align="right">Calories</TableCell>
                      <TableCell align="right">Fat&nbsp;(g)</TableCell>
                      <TableCell align="right">Carbs&nbsp;(g)</TableCell>
                      <TableCell align="right">Protein&nbsp;(g)</TableCell>{" "}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {rows.map((row) => (
                      <TableRow key={row.name}>
                        <TableCell component="th" scope="row">
                          {row.name}
                        </TableCell>
                        <TableCell align="right">{row.calories}</TableCell>
                        <TableCell align="right">{row.fat}</TableCell>
                        <TableCell align="right">{row.carbs}</TableCell>
                        <TableCell align="right">{row.protein}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </StandardCard>
          </Grid>
        </Grid>
      ) : (
        <CenteredCard>
          <Typography variant="h2">
            Sorry, we can't find this stock's information...
          </Typography>
          <Typography>
            Either the symbol "{stockCode}" is not real or it is not currently
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
