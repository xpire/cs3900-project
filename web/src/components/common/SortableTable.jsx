import React from "react";
import {
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Toolbar,
  Typography,
  Tooltip,
  IconButton,
} from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import FilterListIcon from "@material-ui/icons/FilterList";
import OpenInNewIcon from "@material-ui/icons/OpenInNew";
import TradingIcon from "@material-ui/icons/MonetizationOn";
import { Link } from "react-router-dom";

import { ColoredText } from "../common/styled";

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

const EnhancedTableHead = ({ order, orderBy, onRequestSort, headCells }) => {
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox" />
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? "right" : "left"}
            padding={headCell.disablePadding ? "none" : "default"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
};

const EnhancedTableToolbar = ({ title }) => {
  return (
    <Toolbar>
      <Grid
        container
        direction="row"
        justify="space-between"
        alignItems="center"
      >
        <Grid item>
          <Typography variant="h6" id="tableTitle" component="div">
            {title}
          </Typography>
        </Grid>
        <Grid item>
          <Tooltip title="Filter list">
            <IconButton aria-label="filter list">
              <FilterListIcon />
            </IconButton>
          </Tooltip>
        </Grid>
      </Grid>
    </Toolbar>
  );
};

export default function EnhancedTable({ data, header, title }) {
  const [order, setOrder] = React.useState("asc");
  const [orderBy, setOrderBy] = React.useState("calories");

  const handleRequestSort = (_event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  return (
    <div style={{ paddingBottom: "20px" }}>
      <EnhancedTableToolbar title={title} />
      <TableContainer>
        <Table
          aria-labelledby="tableTitle"
          size="medium" // "small"
          aria-label="enhanced table"
        >
          <EnhancedTableHead
            order={order}
            orderBy={orderBy}
            onRequestSort={handleRequestSort}
            rowCount={data.length}
            headCells={header}
          />
          <TableBody>
            {stableSort(data, getComparator(order, orderBy)).map(
              (row, index) => {
                const labelId = `enhanced-table-checkbox-${index}`;
                // const polarity = row.close > row.open;
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={row.name}>
                    <TableCell padding="checkbox" />
                    {header.map(({ id, numeric, disablePadding, color }) => {
                      return (
                        <TableCell
                          component="th"
                          id={labelId}
                          scope="row"
                          align={numeric ? "right" : "left"}
                          padding={disablePadding ? "none" : "default"}
                        >
                          {color ? (
                            <ColoredText color={row[id] > 0 ? "green" : "red"}>
                              {row[id]}
                            </ColoredText>
                          ) : (
                            <>{row[id]}</>
                          )}
                        </TableCell>
                      );
                    })}
                    {/* <TableCell
                      component="th"
                      id={labelId}
                      scope="row"
                      padding="none"
                    >
                      {row.symbol}
                    </TableCell>
                    <TableCell>{row.name}</TableCell>
                    <TableCell align="right">
                      <ColoredText color={polarity ? "green" : "red"}>
                        {row.price}
                      </ColoredText>
                    </TableCell>
                    <TableCell align="right">
                      <ColoredText color={polarity ? "green" : "red"}>
                        {row.open}
                      </ColoredText>
                    </TableCell>
                    <TableCell align="right">
                      <ColoredText color={polarity ? "green" : "red"}>
                        {row.close}
                      </ColoredText>
                    </TableCell>
                    <TableCell align="right">
                      <ColoredText color={polarity ? "green" : "red"}>
                        {row.daily}
                      </ColoredText>
                    </TableCell>
                    <TableCell align="right">
                      <ColoredText color={polarity ? "green" : "red"}>
                        {row.dailyPercentage}
                      </ColoredText>
                    </TableCell> */}
                    <TableCell padding="checkbox">
                      <IconButton component={Link} to={`/stock/${row.symbol}`}>
                        <OpenInNewIcon />
                      </IconButton>
                    </TableCell>
                    <TableCell padding="checkbox">
                      <IconButton
                        component={Link}
                        to={`/trading/${row.symbol}`}
                      >
                        <TradingIcon />
                      </IconButton>
                    </TableCell>
                    <TableCell padding="checkbox">
                      <IconButton
                        onClick={() => console.log(`delete ${row.symbol}`)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                );
              }
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
