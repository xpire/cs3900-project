import React, { useContext } from "react";
import {
  Typography,
  Card,
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
import { ColoredText, CenteredCard } from "../components/common/styled";

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

const StockDetails = (props) => {
  // const { user } = useContext(AuthContext);
  // grab the list of available stocks
  const data = ["AAPL", "TSLA"];
  const stockCode = props.match.params.symbol.toUpperCase();
  return (
    <Page style={{ padding: "20px" }}>
      {data.includes(stockCode) ? (
        <Grid container direction="row" alignItems="stretch">
          <Grid item md={3} sm={5} xs={12}>
            <Card style={{ margin: "10px" }}>
              <Typography variant="h1">{stockCode}</Typography>
              <Typography>Apple Industry</Typography>
              <Chip label="Technology" />
              <ColoredText color="green" variant="h2">
                +20%
              </ColoredText>
            </Card>
          </Grid>
          <Grid item md={9} sm={7} xs={12}>
            <Card style={{ margin: "10px" }}>
              <Typography variant="h1">
                A graph is supposed to be here blah blah blah blah blah
              </Typography>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card style={{ margin: "10px" }}>
              <Typography variant="h3">Hello guys</Typography>
              {/* <TableContainer>
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
            </TableContainer> */}
            </Card>
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
            to="/home"
          >
            Go back
          </Button>
        </CenteredCard>
      )}
    </Page>
  );
};

export default StockDetails;
