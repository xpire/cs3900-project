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
import { format } from "../../utils/formatter";

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
        {/* <Grid item>
          <Tooltip title="Filter list">
            <IconButton aria-label="filter list">
              <FilterListIcon />
            </IconButton>
          </Tooltip>
        </Grid> */}
      </Grid>
    </Toolbar>
  );
};

export default function EnhancedTable({
  data,
  header,
  title,
  handleDelete = null,
  buttons = true,
}) {
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
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={row.name}>
                    {header.map(({ id, numeric, disablePadding, color }) => {
                      const value = numeric ? format(row[id]) : row[id];
                      return (
                        <TableCell
                          component="th"
                          id={labelId}
                          scope="row"
                          align={numeric ? "right" : "left"}
                          padding={disablePadding ? "none" : "default"}
                          key={id}
                        >
                          {color ? (
                            <ColoredText color={value > 0 ? "green" : "red"}>
                              {value > 0 && "+"}
                              {value}
                            </ColoredText>
                          ) : (
                            <>{value}</>
                          )}
                        </TableCell>
                      );
                    })}
                    {buttons && (
                      <>
                        <TableCell padding="checkbox">
                          <Tooltip title="Stock Details">
                            <IconButton
                              component={Link}
                              to={`/stock/${row.symbol}`}
                            >
                              <OpenInNewIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                        <TableCell padding="checkbox">
                          <Tooltip title="Trade">
                            <IconButton
                              component={Link}
                              to={`/trade?symbol=${row.symbol}`}
                            >
                              <TradingIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </>
                    )}
                    {handleDelete && (
                      <TableCell padding="checkbox">
                        <Tooltip title="Remove">
                          <IconButton onClick={() => handleDelete(row)}>
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    )}
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
